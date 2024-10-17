from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
api = Namespace('amenities', description='Amenity operations')
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})
facade = HBnBFacade()
@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        try:
            amenity_data = api.payload
            new_amenity = facade.create_amenity(amenity_data)
            return {"id": new_amenity.id, "name": new_amenity.name}, 201
        except Exception as e:
            return {"message": "Invalid input data"}, 400
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{"id": amenity.id, "name": amenity.name} for amenity in amenities], 200
@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if amenity:
            return {"id": amenity.id, "name": amenity.name}, 200
        return {"message": "Amenity not found"}, 404
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if updated_amenity:
            return {"message": "Amenity updated successfully"}, 200
        return {"message": "Amenity not found"}, 404