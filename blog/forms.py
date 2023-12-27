# blog/forms.py

from werkzeug.routing import ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired
from config import Config


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Content', validators=[DataRequired()])
    is_published = BooleanField('Is Published?')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    @staticmethod
    def validate_username(self, field):
        if field.data != Config.ADMIN_USERNAME:
            raise ValidationError("Invalid username")
        return field.data

    @staticmethod
    def validate_password(self, field):
        if field.data != Config.ADMIN_PASSWORD:
            raise ValidationError("Invalid password")
        return field.data
