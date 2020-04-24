from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, url_for, render_template, redirect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://devo:password@localhost/countries_db'
db = SQLAlchemy(app)
'''class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, username,email):
        self.username=username
        self.email=email
    
    def __repr__(self):
        return '<User %r>'%self.username
 
@app.route('/')
def simple():
    myUser=User.query.all()
    oneItem = User.query.filter_by(username="dev").first()
    return render_template('add_user.html', myUser=myUser, oneItem=oneItem)

@app.route('/post_user', methods=['POST'])
def post_user():
    user=User(request.form['username'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('simple'))'''



@app.route('/map',methods=['GET','POST'])
def my_maps():
    
    mapbox_access_token = 'pk.eyJ1Ijoibm9ub25hbWUiLCJhIjoiY2s4eDkwMm5qMDNsNzNnbnhzenRiMHhzNSJ9.pYTchNKhUZQL-G0HHkZtrg'
    return render_template('murder.html',
        mapbox_access_token=mapbox_access_token,tide='1.24',climate='27')

if __name__ == '__main__':
    app.run(debug=True)