import arrow
import requests
from flask import   session, Blueprint, request, render_template, redirect, flash, url_for, current_app, jsonify, render_template_string
from .forms import CountryForm
from .helperfunc import conversion
#from .helper_func import send_confirmation_email, confirm_token
#from .forms import RegisterForm, SignupForm
from ...models.base import db
from ...models.user import User
from ...models.country import (sites_schema,Sites, site_schema)
from ...secrets import MAPBOX






userRoute = Blueprint('userRoute', __name__)

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
    print(tide_data)








    
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





    #return render_template('api.html', weather_data=weather_data, country=country)

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
    

    
    
    

        #searcher= jsonify({ 'country' : output })
    
        


    return render_template('mapbox.html',mapbox_access_token=MAPBOX,tide='1.24',climate='27', coord=my_coord,
     searcher=searcher1, weather_data=my_weather,sito=sito,coordinator=my_var,tidal=tide,waves=waves)

    
    
    
    
    
    

    
    
