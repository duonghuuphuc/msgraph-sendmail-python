import requests
import json
from flask import Flask, render_template, session, request, redirect, url_for, flash
import forms
from flask_session import Session
from flask_bootstrap import Bootstrap4
import msal
import app_config
import lorem
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime


# initialization
app = Flask(__name__)
app.config.from_object(app_config)
app.config['SECRET_KEY'] = app_config.SECRET_KEY
Session(app)
bootstrap = Bootstrap4(app)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('index.html', user=session["user"], version=msal.__version__)


@app.route("/login")
def login():
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)


@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    try:
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout?post_logout_redirect_uri=" + url_for("index", _external=True))


@app.route("/graphcall")
def graphcall():
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    graph_data = requests.get(  # Use token to call downstream service
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
    ).json()
    return render_template('display.html', result=graph_data, version=msal.__version__)


@app.route("/get-access-token")
def get_access_token():
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    token_type = token['token_type']
    access_token = token['access_token']
    expires_in = token['expires_in']
    return render_template('get_access_token.html', raw_access_token=token, token_type=token_type,
                           access_token=access_token, expires_in=expires_in, version=msal.__version__)


@app.route("/send-mail", methods=['GET', 'POST'])
def send_mail():
    if not session.get("user"):
        return redirect(url_for("login"))

    form = forms.SendMailForm()

    # get from email address (userPrincipalName)
    from_email = _get_user_profile_json()['userPrincipalName']

    if form.validate_on_submit():
        recipient = form.recipient.data
        subject = form.subject.data
        content = form.content.data
        save_to_sent_items = form.save_to_sent_items.data

        # get 'access_token'
        token = _get_token_from_cache(app_config.SCOPE)
        if not token:
            return redirect(url_for("login"))
        access_token = token['access_token']

        # send email
        flag = _send_mail(recipient=recipient, subject=subject, content=content, access_token=access_token,
                          save_to_sent_items=save_to_sent_items)
        if flag:
            flash('Your message has been successfully submitted to the corresponding API.')
        else:
            flash('There is an error that occurred. Please refer to the debug log for more information.')

    # define form default values
    form.subject.data = 'TEST MESSAGE [' + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + ']'
    form.content.data = lorem.paragraph()

    return render_template('send_mail.html', form=form, from_email=from_email, version=msal.__version__)


def _send_mail(recipient, subject, content, access_token, save_to_sent_items=False):
    if recipient is not None and subject is not None and content is not None and access_token is not None:
        user_ms_id = _get_user_profile_json()['id']
        url = 'https://graph.microsoft.com/v1.0/users/' + str(user_ms_id) + '/sendMail'
        print(url)
        payload = json.dumps({
            "message": {
                "subject": str(subject),
                "body": {
                    "contentType": "HTML",
                    "content": str(content)
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": str(recipient)
                        }
                    }
                ]
            },
            "saveToSentItems": str(save_to_sent_items).lower()
        })

        headers = {
            'Authorization': 'Bearer ' + str(access_token),
            'Content-Type': 'application/json'
        }

        # send request
        response = requests.request("POST", url, headers=headers, data=payload)

        # capture response and return to the caller
        print(f"Status Code: {response.status_code}, Response: {response.text}")
        if str(response.status_code) != '202':
            return False
        return True


@app.route('/get-user-profile')
def get_user_profile():
    url = "https://graph.microsoft.com/v1.0/me/"
    payload = {}
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    access_token = token['access_token']
    headers = {
        'Authorization': 'Bearer ' + str(access_token)
    }
    response = requests.request("GET", url, headers=headers, data=payload).json()
    return render_template('get_user_profile.html', user_profile=response)


def _get_user_profile_json():
    url = "https://graph.microsoft.com/v1.0/me/"
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    access_token = token['access_token']
    response = requests.request("GET", url, headers={'Authorization': 'Bearer ' + str(access_token)}).json()
    return response


def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache


def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()


def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)


def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=url_for("authorized", _external=True))


def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result


app.jinja_env.globals.update(_build_auth_code_flow=_build_auth_code_flow)  # Used in template

if __name__ == "__main__":
    app.run()
