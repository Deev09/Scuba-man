# Scuba-man
Scuba-man is a weather monitoring website tailored towards Scuba Divers. The users have the ability to locate their favourite diving location in the US and find it's current weather/ocean/tidal conditions. They also have the option to save their favourite diving location and filter through the the conditions that seem optimal for them to dive in.

The main motivation for this project was to find a way to get real-time data on a specific location and find a way to visualize it on a map. This was inspired by when I went scuba diving and I wanted to know if the conditions were optimal for a dive or not.


# Screenshots
![image](https://user-images.githubusercontent.com/47550028/134714109-ababb4b6-246c-42bd-a3e3-07334512f32c.png)
![image](https://user-images.githubusercontent.com/47550028/134714402-6a83ce5b-8982-4d96-a16f-aea21bb22879.png)



# Tech/framework used
Build with:
- Python Flask
- MapBox
- JavaScript
- PostgreSQL
- Redis
- HTML/CSS



# Installation
To get it running:
- Have python/pip installed
- Clone this github repository : git clone https://github.com/Deev09/Scuba-man.git
- Make a project directory 
- Create a virtual environment for python Flask, this will be where you can store all the packages required for the app to run :https://flask.palletsprojects.com/en/2.0.x/installation/   
- Have PostgreSQL set up 
- Install Redis
- Run migration: db init/ db migrate/ db upgrade
- Run Redis Server/ run rq worker (This should be run from the virtual environment and from the same directory of the project)

# API reference
- https://openweathermap.org/api
- https://api.stormglass.io/v2/tide/extremes/point
- https://api.stormglass.io/v2/weather/point



