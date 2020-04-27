from .base import db, migrate


def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)
