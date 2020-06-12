from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

# https://wtforms.readthedocs.io/en/latest/fields.html
#TODO need etter validators
#https://wtforms.readthedocs.io/en/latest/validators.html#custom-validators

'''class RegisterForm(FlaskForm):
    username = StringField('', validators=[DataRequired()], render_kw = {"placeholder": "Name"})
    email = EmailField('', validators=[DataRequired(), Email()], render_kw = {"placeholder": "Email"})
    submit = SubmitField('Send')

class SignupForm(FlaskForm):
    email = EmailField('', validators=[DataRequired(), Email()], render_kw = {"placeholder": "Email Address..."})
    submit = SubmitField('Get Notified')'''


class CountryForm(Form):
    choices = [('Country', 'Country')]
    select = SelectField('Search for country:', choices=choices)
    search = StringField('')