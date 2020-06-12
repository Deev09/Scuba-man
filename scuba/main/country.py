from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, url_for, render_template, redirect

# the code below is showing the table of countries as my database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://devo:password@localhost/scuba_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    countries_dive_name = db.Column(db.String, unique=True, nullable=False)
    countries_name = db.Column(db.String, nullable=False)
    countries_dive_avg_depth = db.Column(db.String, nullable=False)
    latitude=db.Column(db.String, nullable=False)
    longitude=db.Column(db.String, nullable=False)
# here i'm naming the fields of my database in this function that will call on the main class i.e. connected to my database
    def __init__(self ,countries_name, countries_dive_name, countries_dive_avg_depth, latitude,longitude):
        self.countries_dive_name=countries_dive_name
        self.countries_name=countries_name
        self.countries_dive_avg_depth=countries_dive_avg_depth
        self.latitude=latitude
        self.longitude=longitude
    
db.create_all()   
# this code is to show it on the website
@app.route('/post_user', methods=['POST'])
def post_user():
    user=User(request.form['username'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('simple'))


@app.route('/')
def simple():
    myCountry=Country.query.limit(10).all()
    return render_template('countries.html', myCountry=myCountry)



if __name__ == '__main__':
    app.run(debug=True)