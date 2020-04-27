from flask import session, Blueprint, request, render_template, redirect, flash, url_for, current_app
from ...models.base import db
from ...models.user import User
#from .helper_func import send_confirmation_email, confirm_token
from .forms import RegisterForm, SignupForm
from ...secrets import MAPBOX


userRoute = Blueprint('userRoute', __name__)

@userRoute.route('/')
def home():
    #return '1st working demo'
    form = SignupForm()
    return "TEST Test tESt !!!!"
    #return render_template('index.html', form=form)


@userRoute.route('/map',methods=['GET','POST'])
def my_maps():

    mapbox_access_token = MAPBOX
    return render_template('murder.html',
        mapbox_access_token=mapbox_access_token,tide='1.24',climate='27')
