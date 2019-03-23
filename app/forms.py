from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from sqlalchemy.exc import IntegrityError
from .models import db, User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def get_user(self):
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append("Username not found")
            return None
        if not user.verify_password(self.password.data):
            self.password.errors.append("Invalid password")
            return None
        return user


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("repeat_password", message="Passwords must match"),
        ],
    )
    repeat_password = PasswordField("Repeat Password")

    def create_user(self):
        user = User(username=self.username.data)
        user.password = self.password.data
        db.session.add(user)
        try:
            db.session.commit()
            return user
        except IntegrityError:
            self.username.errors.append("This username is already taken")
            return None


class SetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("repeat_password", message="Passwords must match"),
        ],
    )
    repeat_password = PasswordField("Repeat Password")
