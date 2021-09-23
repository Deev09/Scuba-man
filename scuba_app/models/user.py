from .base import db, login_manager, ma

from flask_login import UserMixin
from .country import sites_schema, Sites, site_schema

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #posts= db.relationship('Sites', secondary=saves, backref=db.backref('saved', lazy= 'dynamic'))
    diving_sites = db.relationship('Sites', backref='diver', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

