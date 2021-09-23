from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from ...models.user import User



class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CountryForm(Form):
    choices = [('Country', 'Country')]
    select = SelectField('Search for country:', choices=choices)
    search = StringField('')

