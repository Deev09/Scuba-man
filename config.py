from scuba_app.secrets import SECRET, POSTGRES_URI
class Config():
    SECRET_KEY = SECRET

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = 'localhost'
    REDIS_PORT = '6379'
    #MAIL_SERVER = ''
    #MAIL_USERNAME = ''
    #MAIL_PASSWORD = ''
    #MAIL_PORT =
    #MAIL_USE_SSL =

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = POSTGRES_URI


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''

