import requests
from flask import Flask,render_template, request
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['DEBUG']=True
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///weather.db'

db=SQLAlchemy(app)
class City(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        new_city= request.form.get('city')

        if new_city:
            new_city_obj=City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()
    #filtering all data
    cities=City.query.all()
    url = 'http://maps.openweathermap.org/maps/2.0/weather/TA2/{0}/{36.778259}/{-119.417931}?appid={230b7544b48513a794a7284e48f2ca6}&fill_bound=true&opacity=0.6&palette=-65:821692;-55:821692;-45:821692;-40:821692;-30:8257db;-20:208cec;-10:20c4e8;0:23dddd;10:c2ff28;20:fff028;25:ffc228;30:fc8014'
    #send request to api and put it in this dictionary

    weather_data=[]
    for city in cities: 


        r=requests.get(url.format(city.name)).json()
        
        weather ={

            'city':city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],

        }

        weather_data.append(weather)

    return render_template('internetweather.html', weather_data=weather_data)
