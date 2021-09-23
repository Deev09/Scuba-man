from scuba_app import create_app
from config import DevConfig
from flask import Flask
from flask_sqlalchemy import SQLAlchemy







if __name__ == '__main__':
    app = create_app(DevConfig)
    
    #app = create_app(DevConfig)
    app.run()
