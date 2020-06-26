import requests
from flask import   session, Blueprint, request, render_template, redirect, flash, url_for, current_app, jsonify
from .forms import CountryForm
#from .helper_func import send_confirmation_email, confirm_token
#from .forms import RegisterForm, SignupForm
from ...models.base import db
from ...models.user import User
from ...models.country import (Country,
                               country_schema,
                               countries_schema)
from ...secrets import MAPBOX






userRoute = Blueprint('userRoute', __name__)

@userRoute.route('/coordinate', methods=['GET', 'POST'])
def coordinata():
    array=[]
    listo=[]




    if request.method=="POST":
        form=request.form
        search_value=form['countries_name']
        search="%{}%".format(search_value)
        coordinate=Country.query.filter(Country.countries_name.like(search)).all()
        #oneItem = Country.query.filter_by(countries_name="Alabama").first()
        def conversion(old):
            direction = {'N':1, 'S':-1, 'E': 1, 'W':-1}
            new = old.replace(u'°',' ').replace('\'',' ').replace('"',' ')
            new = new.split()
            new_dir = new.pop()
            new.extend([0,0,0])
            return (int(float(new[0]))+int(float(new[1]))/60.0+int(float(new[2]))/3600.0) * direction[new_dir]
        for e in coordinate:
            lat, lon = u'''{0}, {1}'''.format(e.latitude, e.longitude).split(', ')
            u=[conversion(lon),conversion(lat)]
            e.latitude=conversion(lat)
            e.longitude=conversion(lon)
            array.append(u)
            listo.append(e.countries_dive_name)

        #return coordinate_var
        #print(coordinate)
        print('it reaches here 1')

        coordinate_output= countries_schema.dump(coordinate)

        session['my_var'] = array
        session['coord_var']= coordinate_output
        print('it reaches here x')

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
    r = requests.get(url.format(cities.countries_name)).json()

    weather = {
        'city' : cities.countries_name,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'],

    }
    weather_data.append(weather)




    return render_template('api.html', weather_data=weather_data, country=country)

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

    output = session.get('coord_var', None)
    my_var = session.get('my_var', None)

    searcher= jsonify({ 'country' : output})

    return render_template('mapbox.html',
        mapbox_access_token=MAPBOX,tide='1.24',climate='27', coord=my_var, searcher=searcher)
