from .base import db, migrate, ma, bcrypt, login_manager


def init_app(app):
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db, ma)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
