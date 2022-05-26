from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Email
from datetime import datetime


class SendMailForm(FlaskForm):
    recipient = StringField('Email', validators=[InputRequired(), Email()])
    subject = StringField('Subject', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()])
    save_to_sent_items = BooleanField("Save this email to Sent folder on the server?", default=False)
    submit = SubmitField('Send')
