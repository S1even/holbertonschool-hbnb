from flask_restx import Api
from .v1.amenities import api as amenities_api

api = Api(
    title='HBnB API',
    version='1.0',
    description='A simple API for the HBnB project',
)

api.add_namespace(amenities_api, path='/api/v1/amenities')