
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
#from forms import RegistrationForm, LoginForm


app = Flask(__name__)


app.config['SECRET_KEY'] = '07fd6b057d48922cf599790213319002'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


from main import routes
