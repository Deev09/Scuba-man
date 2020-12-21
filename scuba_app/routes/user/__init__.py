import arrow
import requests
import datetime
import json
from datetime import datetime
from flask import   session, Blueprint, request, render_template, redirect, flash, url_for, current_app, jsonify, render_template_string
from .forms import CountryForm
from .helperfunc import conversion
# from .helper_func import send_confirmation_email, confirm_token
from .forms import RegisterForm, LoginForm
from ...models.base import db, bcrypt, login_manager, login_user, current_user, logout_user, login_required
from ...models.user import User
from ...models.country import (sites_schema,Sites, site_schema)
from ...secrets import MAPBOX






userRoute = Blueprint('userRoute', __name__)


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
        return redirect(url_for('userRoute.maps'))
    return render_template('signup.html', title='Register', form=form)


@userRoute.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('userRoute.maps'))

# @userRoute.route("/dashboard")
# @login_required
# def dashboard():
#     return render_template('api.html', name=current_user.username)



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
        #coordinate=Sites.query.filter(Sites.site_name.like(search)).all()
        #coordinate= Sites.query.filter_by(countries_name="Alabama").first()
        
        for e in coordinate:
            lat, lon = u'''{0}, {1}'''.format(e.latitude, e.longitude).split(', ')
            u=[conversion(lon),conversion(lat)]
            e.latitude=conversion(lat)
            e.longitude=conversion(lon)
            array.append(u)
            listo.append(e.site_name)

        #return coordinate_var
        #print(coordinate)
        print('it reaches here 1')
 
        coordinate_output= sites_schema.dump(coordinate)

        session['my_var'] = array
        session['coord_var']= coordinate_output
        print('it reaches here x')
        print(array)
        #return redirect(url_for('userRoute.test'))

    print('it reaches here 3x')
    return redirect(url_for('userRoute.maps'))
    #return render_template('countries.html', coordinate=coordinate, lat=conversion(lat), lon=conversion(lon), array=array)






@userRoute.route('/post_user', methods=['GET','POST'])
def post_user():
    myCountry=Sites.query.limit(30).all()

    if request.method=="POST":
        form=request.form
        search_value=form['countries_name']
        search="%{}%".format(search_value)
        arr=Sites.query.filter(Sites.countries_name.like(search)).all()

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
    cities=Sites.query.filter_by(site_name="{}".format(country)).first()

    #state=Sites.query.order_by(Sites.site_name).limit(10).all()
    # statelat=Sites.query.order_by(Sites.latitude).limit(10).all()
    # statelon=Sites.query.order_by(Sites.longitude).limit(10).all()
    # print(statelat, statelon)    
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
            'height': tide_data['data'][i]['height'],
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
    print(waves)
  
    #weather=[{'city' : cities.site_name},{'temperature' : r1['main']['temp']},{'description' : r1['weather'][0]['description']},{'wind_speed':r1['wind']['speed']}]
    weather_data.append(weather)
    print(weather)
    
    session['my_api']=weather
    session['my_coord']=[lon, lat]
    session['my_site_name']=(cities.site_name, cities.countries_dive_avg_depth)
    session['tide']=tidal_arr
    session['waves']=waves
   
    return redirect(url_for('userRoute.maps'))







@userRoute.route('/map/<mappy>',methods=['GET','POST'])
def my_maps(mappy):
    my_var = session.get('my_var', None)
    coord=mappy
    print(mappy)
    print('my_var', my_var)

#    mapbox_access_token = 'pk.eyJ1Ijoibm9ub25hbWUiLCJhIjoiY2s4eDkwMm5qMDNsNzNnbnhzenRiMHhzNSJ9.pYTchNKhUZQL-G0HHkZtrg'
    return render_template('mapbox.html',
        mapbox_access_token=MAPBOX,tide='1.24',climate='27', coord=coord)






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
    
    
    searcher1=(output)
    form = RegisterForm()

    if form.validate_on_submit():
        url="http://maps.openweathermap.org/maps/2.0/weather/TA2/{1}/{23}/{78}?appid=230b7544b48513a794a7284e48f2ca63"
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
 
        #searcher= jsonify({ 'country' : output }) 
    return render_template('mapbox.html',mapbox_access_token=MAPBOX,tide='1.24',climate='27', coord=my_coord,
     searcher=searcher1, weather_data=my_weather,sito=sito,coordinator=my_var,tidal=tide,waves=waves, form=form)

    
    
    
    
    
    

    
    
