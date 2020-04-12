import flask
from flask import request, url_for, render_template, redirect


app = flask.Flask(__name__)

@app.route('/',methods=['GET','POST'])
def my_maps():
    
    mapbox_access_token = 'pk.eyJ1Ijoibm9ub25hbWUiLCJhIjoiY2s4eDkwMm5qMDNsNzNnbnhzenRiMHhzNSJ9.pYTchNKhUZQL-G0HHkZtrg'
    return render_template('murder.html',
        mapbox_access_token=mapbox_access_token,tide='1.24',climate='27')

if __name__ == '__main__':
    app.run(debug=True)