import requests
from flask import   session, Blueprint, request, render_template, redirect, flash, url_for, current_app
from ...models.base import db
from ...models.user import User
from ...models.country import Country

from .forms import CountryForm
#from .helper_func import send_confirmation_email, confirm_token
#from .forms import RegisterForm, SignupForm
from ...secrets import MAPBOX





userRoute = Blueprint('userRoute', __name__)



@userRoute.route('/post_user', methods=['GET','POST'])
def post_user():
    myCountry=Country.query.limit(30).all()
    if request.method=="POST":
        form=request.form
        search_value=form['countries_name']
        search="%{}%".format(search_value)
        arr=Country.query.filter(Country.countries_name.like(search)).all()

        
        #user=request.form["countries_name"]
        return render_template('countries.html', arr=arr)
    else:
        return render_template('filter.html')
    
    #return redirect(url_for('userRoute.simple'))



@userRoute.route('/', methods=['GET']) 
def simple():
    
    #oneItem = Country.query.filter_by(countries_name="Alabama").first()
    #arr=Country.query.filter_by(countries_name="Alabama").all()
    
    return render_template('filter.html' )
    
    

@userRoute.route('/meh/<country>', methods=['GET'])
def index(country):


    
    cities =Country.query.filter_by(countries_name="{}".format(country)).first()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=230b7544b48513a794a7284e48f2ca63'

    weather_data = []
    r = requests.get(url.format(cities.countries_name)).json()

    weather = {
        'city' : cities.countries_name,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'],
        
    }
    weather_data.append(weather)

   


    return render_template('api.html', weather_data=weather_data, country=country)

@userRoute.route('/map',methods=['GET','POST'])
def my_maps():

#    mapbox_access_token = 'pk.eyJ1Ijoibm9ub25hbWUiLCJhIjoiY2s4eDkwMm5qMDNsNzNnbnhzenRiMHhzNSJ9.pYTchNKhUZQL-G0HHkZtrg'
    return render_template('mapbox.html',
        mapbox_access_token=MAPBOX,tide='1.24',climate='27')
