from .base import db, migrate,ma


def init_app(app):
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db, ma)