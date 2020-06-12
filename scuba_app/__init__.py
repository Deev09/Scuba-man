from flask import Flask
from flask_sqlalchemy import SQLAlchemy



def create_app(config_class):
    from . import models, routes

    app = Flask(__name__)
    app.config.from_object(config_class)
    

    models.init_app(app)
    
    routes.init_app(app)
    
   

    # need app_context functionality here
    return app
