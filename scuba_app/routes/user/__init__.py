import os
import re
import arrow
import requests
import datetime
import json
import time
import geojson
from datetime import datetime
from flask import session, Blueprint, request, render_template, redirect, flash, url_for, current_app, jsonify, render_template_string
from redis import Redis
from rq.job import Job
from .forms import CountryForm
from .helperfunc import conversion, tasker
from pathlib import Path
# from .helper_func import send_confirmation_email, confirm_token
from .forms import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required,AnonymousUserMixin
from ...models.base import db, bcrypt, login_manager
from ...models.user import User
from ...models.country import (sites_schema, Sites, site_schema)
from ...secrets import MAPBOX, OPENWEATHER_ID, TIDE_AUTH_ID

# this fetches the job id required for catching with Redis to call multipl API
def background_task(n):
    delay=2
    print("Task running")
    print(f"Simulating {delay} second delay")

    time.sleep(delay)
    print(len(n))
    print("Task Complete")

    return len(n)
    
 


# this class shows Guest when no user is logged in
class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.username = 'Guest'




userRoute = Blueprint('userRoute', __name__)




# this functions fetches the id and returns it as a simple string for other routes to use
@userRoute.route("/task")
def task():
    job = tasker()
    print('Job id: %s' % job.id)
    print('reached here')
    return 'Job id: {}'.format(job.id)


# this function gets the job id, writes to a JSON file and appends new data to the JSON file for the map
@userRoute.route("/geojson/<jobid>")
def geojson_submit(jobid):
    redis_conn = Redis()
    
    job = Job.fetch(jobid, connection=redis_conn)
    allapi=job.result
    print(len(allapi))
    # Opening JSON file 

    # f = open('/Users/assswain/Desktop/projects/Scuba-man/scuba_app/routes/user/sitee.json',) 
    f = open('/Users/deevyaswain/Desktop/projects/Scuba/Scuba-man/scuba_app/routes/user/sitee.json',) 
    
    # returns JSON object as a dictionary 
    data = json.load(f) 
    
    # Iterating through the json 
    # list 
   
    
    # Closing file 
    f.close()
    site=json.dumps(data)
    

    for i, data_point in enumerate(allapi):
        d1=data['features'][i]['properties']
        d2=allapi[i]
        d1['city']=d2['city']
        d1['description']=d2['description']
        d1['temperature']=d2['temperature']
        d1['wind_speed']=d2['wind_speed']
    
    # with open('/Users/assswain/Desktop/projects/Scuba-man/scuba_app/routes/user/sitee_update.json', 'w', encoding='utf-8') as f:
    with open('/Users/deevyaswain/Desktop/projects/Scuba/Scuba-man/scuba_app/routes/user/sitee_update.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
   

    print(type(data))

       

    return redirect(url_for('userRoute.maps'))
    






@userRoute.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    user = User.query.filter_by(email=form.email.data).first()
    # if the hashed password matches the one typed in by the user
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('userRoute.maps'))
    else:
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@userRoute.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('userRoute.login'))
    return render_template('signup.html', title='Register', form=form)


@userRoute.route("/logout")
def logout():
    login_manager.anonymous_user = Anonymous
    logout_user()
    return redirect(url_for('userRoute.maps'))



# helps in converting the GPS coordinate to normal lat long for the map to understand
@userRoute.route('/coordinate', methods=['GET', 'POST'])
def coordinata():
    array=[]
    listo=[]


    if request.method=="POST":
        form=request.form
        search_value=form['countries_name']
        print(search_value)
        search="%{}%".format(search_value)
        
        coordinate=Sites.query.filter(Sites.countries_name.like(search)).all()
       
        for e in coordinate:
            lat, lon = u'''{0}, {1}'''.format(e.latitude, e.longitude).split(',')
            u=[conversion(lon),conversion(lat)]
            e.latitude=conversion(lat)
            e.longitude=conversion(lon)
            array.append(u)
            listo.append(e.site_name)

 
        coordinate_output= sites_schema.dump(coordinate)

        session['my_var'] = array
        session['coord_var']= coordinate_output
        print(array)
   
    return redirect(url_for('userRoute.maps'))
    





@userRoute.route('/', methods=['GET'])
def simple():
    return redirect(url_for('userRoute.login'))





# this function handles all the api calls
@userRoute.route('/meh/<country>', methods=['GET'])
def index(country):
    cities=Sites.query.filter_by(site_name="{}".format(country)).first()
#    url from an api
    url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}'
    

    weather_data = []
    lat=conversion(cities.latitude)
    lon=conversion(cities.longitude)
    print(lat, lon, 'string : latlong')
    
    # gathering the data from the api by sending in the latitude and logitude from the previous function 
    r1 =requests.get(url.format(lat,lon, OPENWEATHER_ID)).json()
    

    weather = { 
        'city' : cities.site_name,
        'temperature' : r1['main']['temp'],
        'description' : r1['weather'][0]['description'],
        'wind_speed': r1['wind']['speed'],
    }
 
    start = arrow.now().floor('day')
    end = arrow.now().shift(days=1).floor('day')
# this is used for authorizing with stormglass to use the API
    response1 = requests.get(
    'https://api.stormglass.io/v2/tide/extremes/point',
    params={
        'lat': lat,
        'lng': lon,
        'start': start.to('UTC').timestamp,  # Convert to UTC timestamp
        'end': end.to('UTC').timestamp,  # Convert to UTC timestam
    },
    headers={
        'Authorization': TIDE_AUTH_ID
    }
    )
    tide_data = response1.json()
    tidal_arr=[]
    for i in range(2):
        tidal={
            'height': "{:.2f}".format(tide_data['data'][i]['height']),
            'time': tide_data['data'][i]['time'],
            'type': tide_data['data'][i]['type'],
        }
        tidal_arr.append(tidal)
    #print(tide_data)
    
    response2 = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat': lat,
            'lng': lon,
            'params': ['waterTemperature'],
             # Convert to UTC timestamp
        },
        headers={
            'Authorization': TIDE_AUTH_ID
        }
        )
    wave_data=response2.json()
    
    waves={'water_temperature': wave_data['hours'][0]['waterTemperature']['noaa']}
    
    weather_data.append(weather)
    diving_site=weather['city']
    print(tidal_arr)
   
    # all of these sessions are passed around to different functions for a wuick method of sending data
    
    session['my_api_site']=diving_site
    session['my_api']=weather
    session['my_coord']=[lon, lat]
    session['my_site_name']=(cities.site_name, cities.countries_dive_avg_depth)
    session['tide']=tidal_arr
    session['waves']=waves
   
    return redirect(url_for('userRoute.maps'))



# this functions helps in storing user information by linking the sites database to the user database so that the user can store multipls locations
@userRoute.route('/save', methods=['GET'])
@login_required
def saveSite():
    site_name=session.get('my_api_site',[{1:1},{2:2}])
    site_obj=Sites.query.filter_by(site_name="{}".format(site_name)).first()
    print(site_obj.site_name)
    user_obj = User.query.filter_by(username=current_user.username).first_or_404()
    print('appending to user_obj')
    user_obj.diving_sites.append(site_obj)
    db.session.commit()
    print('saved diving site successfully')

    print(user_obj.diving_sites)
    return redirect(url_for('userRoute.maps'))


# this shows the stores location from the current usre as a json file
@userRoute.route('/display_location')
@login_required
def display_sites():
    user_obj = User.query.filter_by(username=current_user.username).first_or_404()
    site_names=[]
    for site in user_obj.diving_sites:
        print(site.site_name)
        site_names.append(site.site_name)
    return json.dumps(site_names)





# this is the main route that calles to the html page that displays the map and coordinates
@userRoute.route('/map',methods=['GET','POST'])

def maps():
 
    
    output = session.get('coord_var', [{1:1},{2:2}])
    my_var = session.get('my_var', None)
    my_weather=session.get('my_api',[{1:1},{2:2}])
    my_coord=session.get('my_coord', None)
    sito=session.get('my_site_name',None)
    tide=session.get('tide',[{1:1},{2:2}])
    waves=session.get('waves',[{1:1},{2:2}])
    
    # Opening JSON file 
    f = open('/Users/deevyaswain/Desktop/projects/Scuba/Scuba-man/scuba_app/routes/user/sitee_update.json',) 
 
    data = json.load(f) 

    f.close()

    searcher1=(output)
    form = RegisterForm()
    



    if form.validate_on_submit():
        
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
 
        #searcher= jsonify({ 'country' : output }) 
    return render_template('mapbox.html',mapbox_access_token=MAPBOX,tide='1.24',climate='27', coord=my_coord,
     searcher=searcher1, weather_data=my_weather,sito=sito,coordinator=my_var,tidal=tide,waves=waves, form=form, name=current_user.username, addedapi=data)

    
    
    
    
    
    

    
    
