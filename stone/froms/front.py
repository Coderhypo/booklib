from sanic_wtf import SanicForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from stone.models.user import User


class LoginForm(SanicForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

    def validate_password(self, field):
        email = self.email.data
        password = field.data
        user = User.query.filter_by(email=email).first()
        if not user or user.check_password(password):
            raise ValidationError("Wrong email or password")


class RegisterForm(SanicForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    re_password = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_email(self, field):
        email = self.email.data
        user = User.query.filter_by(email=email).first()
        if not user:
            return
        raise ValidationError("Email already exist.")

