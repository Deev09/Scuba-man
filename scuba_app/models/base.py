from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required




db = SQLAlchemy()
ma= Marshmallow()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager= LoginManager()

