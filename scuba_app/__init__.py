from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
import rq



def create_app(config_class):
    from . import models, routes

    app = Flask(__name__)
    app.config.from_object(config_class)
    #app.redis = Redis(app.config['REDIS_HOST'], app.config['REDIS_PORT'])
    #app.task_queue = rq.Queue(connection=app.redis)

    models.init_app(app)
    
    routes.init_app(app)
    
   

    # need app_context functionality here
    return app
