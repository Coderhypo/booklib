from sanic_wtf import SanicForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class LoginForm(SanicForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

    def validate_password(self, field):
        email = self.email.data
        password = field.date


class RegisterForm(SanicForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    re_password = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])

    def validate_email(self, field):
        email = self.email.data

