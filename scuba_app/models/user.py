from .base import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True) #nullable=Flase
    email = db.Column(db.String(64), unique=True, index=True) #nullable=False
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirm_date = db.Column(db.DateTime, nullable=True) #TODO use this in confir_token


    def __init__(self, email):
        self.email = email

    @property
    def is_authenticated(self):
        #Return True if the user is authenticated
        return #self.authenticated

    def generate_auth_token(self, expires_in, app):
        return

    @staticmethod
    def verify_auth_token(token):
        return
