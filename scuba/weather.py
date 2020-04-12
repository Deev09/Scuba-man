from main import app
import requests
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


@app.route('/weather')
def index():
    return render_template('weather.html')
if __name__ == '__main__':
    app.run(debug=True)