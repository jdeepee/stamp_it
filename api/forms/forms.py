from wtforms import Form, BooleanField, TextField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from wtforms import validators

class SignUpForm(Form):
	username = TextField('username', [validators.Required(), validators.Length(min=4, max=25)])
	name = TextField('name', [validators.Required(), validators.Length(min=4, max=25)])
	email = EmailField('email', [validators.Required(), validators.Length(min=4, max=25)])
	password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	accept_tos = BooleanField('I accept the TOS', [validators.Required()])

class CompanySignUpForm(Form):
	name = TextField('name', [validators.Required(), validators.Length(min=2, max=25)])

class LoginForm(Form):
	email = EmailField('email', [validators.Required(), validators.Length(min=4, max=25)])
	password = PasswordField('password', [validators.Required()])