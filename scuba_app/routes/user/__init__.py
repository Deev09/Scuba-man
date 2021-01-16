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
# from .helper_func import send_confirmation_email, confirm_token
from .forms import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required,AnonymousUserMixin
from ...models.base import db, bcrypt, login_manager
from ...models.user import User
from ...models.country import (sites_schema, Sites, site_schema)
from ...secrets import MAPBOX


def background_task(n):
    delay=2
    print("Task running")
    print(f"Simulating {delay} second delay")

    time.sleep(delay)
    print(len(n))
    print("Task Complete")

    return len(n)
    
 



class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.username = 'Guest'




userRoute = Blueprint('userRoute', __name__)



@userRoute.route('/getdata', methods=['GET','POST'])
def get_javascript_data():
    
    if request.method == 'GET':
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        names = request.get_json()
        
        # parse as JSON
        return 'Sucesss', 200 ,names




@userRoute.route('/map_update', methods=['GET','POST'])
def map_update():
    return 'meh'

@userRoute.route("/task")
def task():
    job = tasker()
    print('Job id: %s' % job.id)
    print('reached here')
    return 'Job id: {}'.format(job.id)



@userRoute.route("/fetch/<jobid>")
def fetch_job(jobid):
    redis_conn = Redis()
    job = Job.fetch(jobid, connection=redis_conn)
    print(job)
    print('Status: %s' % job.get_status())
    #print(job.result)
    site=job.result
    # jsonify(site)
    site_list=json.dumps(site)
    session['my_allapi'] = site
    
    return site_list

 
@userRoute.route("/geojson", methods=['GET','POST'])
def geojson_submit():
    allapi=session.get('my_allapi',[{1:1},{2:2}])
    # Opening JSON file 
    f = open('/Users/assswain/Desktop/projects/Scuba-man/scuba_app/routes/user/sitee.json',) 
    
    # returns JSON object as  
    # a dictionary 
    data = json.load(f) 
    
    # Iterating through the json 
    # list 
   
    
    # Closing file 
    f.close()
    site=json.dumps(data)
    

    for i in range(3):
        d1=data['features'][i]['properties']
        d2=allapi[i]
        d1['city']=d2['city']
        d1['description']=d2['description']
        d1['temperature']=d2['temperature']
        d1['wind_speed']=d2['wind_speed']
        # print(d2['city'], d2['description'], d2['temperature'], d2['wind_speed'])
        # print(d1)
    with open('/Users/assswain/Desktop/projects/Scuba-man/scuba_app/routes/user/sitee_update.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    #added_weather=json.dumps(data['features'])
    #session['added_geojson'] = added_weather

    print(type(data))

       

    return redirect(url_for('userRoute.maps'))
    



@userRoute.route('/capabilities', methods=['GET','POST'])
def capabilities():
    token=requests.get(
        'https://pfa.foreca.com/authorize/token?expire_hours=4',
        params={
            'expire_hours': 4,
            'user': 'deevya-swain',
            'password': 'ZqdCCicyBPHvExdX2P'
        },

    )
    rawr=token.json()
    print(rawr['access_token'])
    responder = requests.get(
        'https://map-eu.foreca.com/api/v1/capabilities',
        
        headers={
            'Authorization': 'Bearer {}'.format(rawr['access_token'])
           
        }
        )
    layer_data=responder.json()
    time_data_0 = layer_data["images"][0]["times"]["available"][0]

    url_endpoint = "https://map-eu.foreca.com/api/v1/image/tile/4/9/3/2020-12-20T03:00:00Z/2"
    #data = {}
    headers = {"Authorization" : "Bearer {}".format(rawr['access_token'])}
    #mapper =  json.dumps(requests.get(url_endpoint, headers=headers))
    #print(mapper)
    return layer_data


@userRoute.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    user = User.query.filter_by(email=form.email.data).first()
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
    # if current_user.is_authenticated:
    #     return redirect(url_for('userRoute.maps'))
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



@userRoute.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


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






@userRoute.route('/meh/<country>', methods=['GET'])
def index(country):
    cities=Sites.query.filter_by(site_name="{}".format(country)).first()
   
    url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid=230b7544b48513a794a7284e48f2ca63'

    weather_data = []
    lat=conversion(cities.latitude)
    lon=conversion(cities.longitude)
    print(lat, lon, 'string : latlong')
    
    #r = requests.get(url.format(cities.countries_name)).json()
    r1 =requests.get(url.format(lat,lon)).json()
    

    weather = { 
        'city' : cities.site_name,
        'temperature' : r1['main']['temp'],
        'description' : r1['weather'][0]['description'],
        'wind_speed': r1['wind']['speed'],
    }
 
    start = arrow.now().floor('day')
    end = arrow.now().shift(days=1).floor('day')

    response1 = requests.get(
    'https://api.stormglass.io/v2/tide/extremes/point',
    params={
        'lat': lat,
        'lng': lon,
        'start': start.to('UTC').timestamp,  # Convert to UTC timestamp
        'end': end.to('UTC').timestamp,  # Convert to UTC timestam
    },
    headers={
        'Authorization': '4604db58-c6ab-11ea-870a-0242ac130002-4604dc5c-c6ab-11ea-870a-0242ac130002'
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
            'Authorization': '4604db58-c6ab-11ea-870a-0242ac130002-4604dc5c-c6ab-11ea-870a-0242ac130002'
        }
        )
    wave_data=response2.json()
    
    waves={'water_temperature': wave_data['hours'][0]['waterTemperature']['noaa']}
    #waves_arr.append(waves)
    # print(waves)
    #print('https://api.stormglass.io/v2/weather/point?lat=37.78333333333333&lng=-119.05')
  
    #weather=[{'city' : cities.site_name},{'temperature' : r1['main']['temp']},{'description' : r1['weather'][0]['description']},{'wind_speed':r1['wind']['speed']}]
    weather_data.append(weather)
    diving_site=weather['city']
    print(tidal_arr)
    # print(weather_data)

    # print(diving_site)
    
    
    session['my_api_site']=diving_site
    session['my_api']=weather
    session['my_coord']=[lon, lat]
    session['my_site_name']=(cities.site_name, cities.countries_dive_avg_depth)
    session['tide']=tidal_arr
    session['waves']=waves
   
    return redirect(url_for('userRoute.maps'))




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



@userRoute.route('/display_location')
@login_required
def display_sites():
    user_obj = User.query.filter_by(username=current_user.username).first_or_404()
    site_names=[]
    for site in user_obj.diving_sites:
        print(site.site_name)
        site_names.append(site.site_name)
    return json.dumps(site_names)


# @userRoute.route('/map/<mappy>',methods=['GET','POST'])
# def my_maps(mappy):
#     my_var = session.get('my_var', None)
#     coord=mappy
#     print(mappy)
#     print('my_var', my_var)

# #    mapbox_access_token = 'pk.eyJ1Ijoibm9ub25hbWUiLCJhIjoiY2s4eDkwMm5qMDNsNzNnbnhzenRiMHhzNSJ9.pYTchNKhUZQL-G0HHkZtrg'
#     return render_template('mapbox.html',
#         mapbox_access_token=MAPBOX,tide='1.24',climate='27', coord=coord)






@userRoute.route('/map',methods=['GET','POST'])

def maps():
    #searcher1=[{1:1},{2:2}]
    
    output = session.get('coord_var', [{1:1},{2:2}])
    my_var = session.get('my_var', None)
    my_weather=session.get('my_api',[{1:1},{2:2}])
    my_coord=session.get('my_coord', None)
    sito=session.get('my_site_name',None)
    tide=session.get('tide',[{1:1},{2:2}])
    waves=session.get('waves',[{1:1},{2:2}])
    
    # Opening JSON file 
    f = open('/Users/assswain/Desktop/projects/Scuba-man/scuba_app/routes/user/sitee_update.json',) 
 
    data = json.load(f) 

    f.close()
    site=json.dumps(data)

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

    
    
    
    
    
    

    
    
