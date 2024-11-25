"""
This module defines the API endpoints for managing amenities using Flask-RESTx.

Endpoints:
    - /amenities/: Allows listing all amenities and creating a new amenity.
    - /amenities/<amenity_id>: Allows retrieving, updating, and managing a specific amenity.
"""


from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.services.facade import HBnBFacade


api = Namespace('amenities', description='Amenity operations')


amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


facade = HBnBFacade()


@api.route('/')
class AmenityList(Resource):
    """
    Resource class for handling amenity collections.

    Methods:
        post: Create a new amenity.
        get: Retrieve a list of all amenities.
    """


    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized - Admin access required')
    def post(self):
        """
        Create a new amenity.

        This endpoint requires a valid JWT token. Admin privileges are required to create an amenity.

        Returns:
            dict: Details of the created amenity.
            HTTP Status: 201 if successful, 400 or 403 otherwise.
        """

        data = get_jwt_identity()

        data = api.payload

        try:
            amenity = facade.create_amenity(data)
            return {
                'id': amenity.id,
                'name': amenity.name
            }, 201

        except ValueError as e:
            return {'message': str(e)}, 400

        except Exception:
            return {'message': 'Failed to create amenity'}, 400


    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve a list of all amenities.

        Returns:
            list: A list of all amenities with their details.
            HTTP Status: 200.
        """

        amenities = facade.get_all_amenities()
        return [{'id': amenity.id, 'name': amenity.name} for amenity in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """
    Resource class for handling individual amenities.

    Methods:
        get: Retrieve details of a specific amenity.
        put: Update an existing amenity.
    """


    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Retrieve details of a specific amenity by ID.

        Args:
            amenity_id (str): The ID of the amenity to retrieve.

        Returns:
            dict: Details of the requested amenity.
            HTTP Status: 200 if successful, 404 if not found.
        """

        try:
            amenity = facade.get_amenity(amenity_id)
            return {'id': amenity.id, 'name': amenity.name}, 200

        except ValueError as e:
            return {'message': str(e)}, 404


    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized - Admin access required')
    def put(self, amenity_id):
        """
        Update an existing amenity.

        This endpoint requires a valid JWT token. Admin privileges are required to update an amenity.

        Args:
            amenity_id (str): The ID of the amenity to update.

        Returns:
            dict: A message indicating the result of the operation.
            HTTP Status: 200 if successful, 400 or 404 otherwise.
        """

        current_user = get_jwt_identity()

        if not current_user.get('is_admin'):
            return {'message': 'Admin access required'}, 403

        try:
            updated_amenity = facade.update_amenity(amenity_id, api.payload)
            return {'message': 'Amenity updated successfully'}, 200

        except ValueError as e:
            return {'message': str(e)}, 400 if 'Invalid' in str(e) else 404