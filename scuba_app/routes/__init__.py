from .user import userRoute
#from .init_ext import mail

def init_app(app):
    #mail.init_app(app)
    app.register_blueprint(userRoute)
