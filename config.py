class Config():
    SECRET_KEY = '378f9b8d99211b55f74229568e4a732b' 

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
    SQLALCHEMY_DATABASE_URI = 'postgresql://mask:password@localhost/scubapp_db'
    


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''

