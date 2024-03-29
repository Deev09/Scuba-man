from .base import db, login_manager, ma
#from ..routes .user .forms import UserMixin
#from .user import User
#from marshmallow_sqlalchemy import ModelSchema


class Sites(db.Model):
    __tablename__ = 'sites'
    id = db.Column(db.Integer, primary_key=True)
    site_name=db.Column(db.String, unique=True)
    countries_name = db.Column(db.String, nullable=False)
    countries_dive_avg_depth = db.Column(db.String, nullable=False)
    latitude=db.Column(db.String, nullable=False)
    longitude=db.Column(db.String, nullable=False)
    diver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __init__(self ,countries_name, countries_dive_name, countries_dive_avg_depth, latitude,longitude):
        self.site_name=countries_dive_name
        self.countries_name=countries_name
        self.countries_dive_avg_depth=countries_dive_avg_depth
        self.latitude=latitude
        self.longitude=longitude

    def __repr__(self):
        return '<Sites %r>'%self.site_name

    

    

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



class SitesSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'site_name',
            'countries_dive_avg_depth',
            'latitude',
            'longitude',
            'countries_name'
        )


sites_schema=SitesSchema(many=True)
site_schema=SitesSchema()