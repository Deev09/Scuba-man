from .base import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, username,email):
        self.username=username
        self.email=email

    def __repr__(self):
        return '<User %r>'%self.username
        