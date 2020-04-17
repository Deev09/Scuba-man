from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, url_for, render_template, redirect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://devo:password@localhost/scuba_db'
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)


db.session.add(User(username="Flask", email="example@example.com"))
db.session.commit()

users = User.query.all()

'''@app.route('/',methods=['GET','POST'])
def my_maps():
    
    mapbox_access_token = 'pk.eyJ1Ijoibm9ub25hbWUiLCJhIjoiY2s4eDkwMm5qMDNsNzNnbnhzenRiMHhzNSJ9.pYTchNKhUZQL-G0HHkZtrg'
    return render_template('murder.html',
        mapbox_access_token=mapbox_access_token,tide='1.24',climate='27')'''

if __name__ == '__main__':
    app.run(debug=True)