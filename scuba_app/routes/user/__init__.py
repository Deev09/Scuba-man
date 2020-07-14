import requests
from flask import   session, Blueprint, request, render_template, redirect, flash, url_for, current_app, jsonify, render_template_string
from .forms import CountryForm
from .helperfunc import conversion
#from .helper_func import send_confirmation_email, confirm_token
#from .forms import RegisterForm, SignupForm
from ...models.base import db
from ...models.user import User
from ...models.country import (Country,
                               country_schema,
                               countries_schema, SitesSchema,Sites, site_schema)
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
        trial=Country.query.filter_by(countries_name="Alabama")
        print(trial.id)
        
        
        
        coordinate=Sites.query.filter(Country.countries_name.like(search)).all()
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
        print(listo)
        print(coordinate)
        

        coordinate_output= countries_schema.dump(coordinate)

        #session['my_var'] = array
        session['coord_var']= coordinate_output
        print('it reaches here x')
        print(coordinate_output)

        #return redirect(url_for('userRoute.test'))

    print('it reaches here 3x')
    return redirect(url_for('userRoute.maps'))
    #return render_template('countries.html', coordinate=coordinate, lat=conversion(lat), lon=conversion(lon), array=array)


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

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=230b7544b48513a794a7284e48f2ca63'

    weather_data = []
    lat=conversion(cities.latitude)
    lon=conversion(cities.longitude)
    
    r = requests.get(url.format(cities.countries_name)).json()

    '''weather = { 
        'city' : cities.countries_name,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        

    }'''
    weather=[{'city' : cities.countries_name},{'temperature' : r['main']['temp']},{'description' : r['weather'][0]['description']}]
    weather_data.append(weather)
    print(weather_data)
    
    session['my_api']=weather
    session['my_coord']=[lon, lat]
    print(lat, lon, 'string : latlong')
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
    #my_var = session.get('my_var', None)
    my_weather=session.get('my_api',[{1:1},{2:2}])
    my_coord=session.get('my_coord', None)
    searcher1=(output)
    

    
    
    

        #searcher= jsonify({ 'country' : output })
    
        


    return render_template('mapbox.html',
        mapbox_access_token=MAPBOX,tide='1.24',climate='27', coord=my_coord, searcher=searcher1, weather_data=my_weather)

    
    
    
    
    
    

    
    
