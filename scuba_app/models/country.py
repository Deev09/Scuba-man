from .base import db
from .base import ma
#from marshmallow_sqlalchemy import ModelSchema

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #countries_dive_avg_depth = db.Column(db.String, nullable=False)
    countries_name = db.Column(db.String, nullable=False)
    #countries_dive_avg_depth = db.Column(db.String, nullable=False)
    countries_dive_name = db.relationship('Sites', backref='country', lazy=True)
    #latitude=db.Column(db.String, nullable=False)
    #longitude=db.Column(db.String, nullable=False)
# here i'm naming the fields of my database in this function that will call on the main class i.e. connected to my database
    def __init__(self ,countries_name, countries_dive_name, countries_dive_avg_depth, latitude,longitude):
        self.countries_dive_name=countries_dive_name
        self.countries_name=countries_name
        #self.countries_dive_avg_depth=countries_dive_avg_depth
        #self.latitude=latitude
        #self.longitude=longitude
    def __repr__(self):
        return '<Country %r>'%self.countries_dive_name

class Sites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name=db.Column(db.String, unique=True)
    countries_dive_avg_depth = db.Column(db.String, nullable=False)
    latitude=db.Column(db.String, nullable=False)
    longitude=db.Column(db.String, nullable=False)
    country_id=db.Column(db.Integer, db.ForeignKey('country.id'))
    

'''
class CountrySchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'countries_dive_name',
            'countries_name',
            'countries_dive_avg_depth',
            'latitude',
            'longitude'
        )
'''


class CountrySchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'countries_dive_name',
            'countries_name',
            
            
        )
class SitesSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'countries_dive_name',
            'countries_dive_avg_depth',
            'latitude',
            'longitude'
        )

country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)
sites_schema=SitesSchema(many=True)
site_schema=SitesSchema()