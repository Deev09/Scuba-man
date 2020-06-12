class Config():
    SECRET_KEY = 'some_secret_key_you_name_it'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #MAIL_SERVER = ''
    #MAIL_USERNAME = ''
    #MAIL_PASSWORD = ''
    #MAIL_PORT =
    #MAIL_USE_SSL =

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://mask:password@localhost/scubapp_db'


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''

