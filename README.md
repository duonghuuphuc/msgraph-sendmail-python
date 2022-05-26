# Send mails with Microsoft Graph & authorized with OAuth 2.0

In this repository, I will share a Flask application that authorizes users having either personal Microsoft accounts (Skype, Xbox, Live, and Hotmail) or Microsoft business accounts. The demo application also presents an email composer form to send emails on behalf of the authorized users.


## API functionality demonstrated in this sample

 - Log-in users with Microsoft OAuth2
 - Retrieve users' information with Microsoft Azure Active Directory
 - Send mail on behalf of the users

## Prerequisite

 - A Microsoft 365 account with an active subscription such as Home or Business plan
 - If you are trying this tutorial within an organization that subscribes to Microsoft 365 Business plan, you also need to have an Administrator account to grant permissions on the created application
 - You should have a background in Python programming language to understand the sample Flask project.

## Step-by-step tutorials

I have an article to present the procedure to authorize a client program that sends emails on behalf of users that have either a personal Microsoft account or a business one. The procedure consists of four main steps, i.e., (1) create an application on Microsoft Azure, (2) issue credentials, (3) add API permissions to the application, and (4) run the demo program.

Read the article at https://www.duonghuuphuc.com/sites/dev/msgraph-sendmail-python-en.html

## TL;DR

You can jump right into the demo by performing the following steps:

 1. Register an application on [Microsoft Azure](https://go.microsoft.com/fwlink/?linkid=2083908)
 2. Create application credentials on Microsoft Azure
 3. Grant API permissions: `Mail.Send`, `User.Read`, `User.ReadBasic.All`
 4. Clone the demo project from this repository
 5. Configure `CLIENT_ID` and `CLIENT_SECRET` in the **env.sh** file
 6. [Optional] Create a new Python environment to avoid any errors in your current working environment
 7. Install required packages by executing this command in an activated Python environment: `pip install -r requirements.txt`
 8. Run the project by executing this command: `source env.sh`

*Note: step #7 is performed only one time.*

## Application screenshots

![Fig. 1. Homepage of the demo Flask project for anonymous users](https://www.duonghuuphuc.com/sites/dev/static/img/20220526A/app-screenshot-01.png)

![Fig. 2. Homepage of the demo Flask project for authenticated users](https://www.duonghuuphuc.com/sites/dev/static/img/20220526A/app-screenshot-02.png)

![Fig. 3. Get user profile. The API returns the following attributes: businessPhones, displayName, givenName, id, jobTitle, mail, mobilePhone, officeLocation, preferredLanguage, surname, userPrincipalName](https://www.duonghuuphuc.com/sites/dev/static/img/20220526A/app-screenshot-03.png?)

![Fig. 4. Send email form](https://www.duonghuuphuc.com/sites/dev/static/img/20220526A/app-screenshot-04.png)

![Fig. 5. Get and render the Access Token on a web page](https://www.duonghuuphuc.com/sites/dev/static/img/20220526A/app-screenshot-05.png)

## Known issues

 - If you run this sample project on a web server on a home network without a static IP address and/or without an assigned domain name, you may need to use a [DDNS](https://www.cloudflare.com/learning/dns/glossary/dynamic-dns/) provider, and then forward the corresponding network ports to your web server.

## Further Reading

 - Tutorial: [Microsoft Graph — Send Mail API](https://www.duonghuuphuc.com/sites/dev/msgraph-sendmail-python-en.html)
 - Tutorial: [Microsoft Graph — Single Sign-on](https://www.duonghuuphuc.com/sites/dev/msgraph-sso-python-en.html)
 - [Microsoft Azure - Authentication vs. authorization](https://docs.microsoft.com/en-us/azure/active-directory/develop/authentication-vs-authorization)
 - [Microsoft Authentication Library (MSAL) for Python](https://docs.microsoft.com/en-us/python/api/overview/azure/active-directory?view=azure-python)
 - [Azure Active Directory B2C](https://azure.microsoft.com/en-us/services/active-directory/external-identities/b2c/#overview)

## Contributors

 - Phuc H. Duong / [www.duonghuuphuc.com](https://www.duonghuuphuc.com/) / `dhpit [at] m.dhpit.com`

