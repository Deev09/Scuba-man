import requests
import time
from redis import Redis
from rq import Queue
from ...models.country import Sites
from ...secrets import OPENWEATHER_ID

redis_conn = Redis()
q = Queue(connection=redis_conn)

def conversion(old):
    direction = {'N':1, 'S':-1, 'E': 1, 'W':-1}
    new = old.replace(u'°',' ').replace('\'',' ').replace('"',' ')
    new = new.split()
    new_dir = new.pop()
    new.extend([0,0,0])
    return (int(float(new[0]))+int(float(new[1]))/60.0+int(float(new[2]))/3600.0) * direction[new_dir]


def tasker():
    cities=Sites.query.all()
    job = q.enqueue(get_request_lalong, cities, job_timeout=1000, result_ttl=10000)
    return job

def get_request_lalong(cities):
    temp_arr = []
    url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}'
    for city in cities:
        lat=conversion(city.latitude)
        lon=conversion(city.longitude)
        r1 = requests.get(url.format(lat,lon, OPENWEATHER_ID)).json()
        weather = { 
            'city' : city.site_name,
            'temperature' : r1['main']['temp'],
            'description' : r1['weather'][0]['description'],
            'wind_speed': r1['wind']['speed'],
        }
        temp_arr.append(weather)
        #time.sleep(1)
    return temp_arr