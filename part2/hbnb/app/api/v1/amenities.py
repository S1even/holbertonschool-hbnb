from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade


api = Namespace('amenities', description='Amenity operations')


amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


facade = HBnBFacade()


@api.route('/')
class AmenityList(Resource):
    """
    Resource for handling requests for a list of amenities and creating new amenities.
    """

    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new amenity.
        
        This method handles the POST request to create a new amenity. It expects
        the payload to match the `amenity_model`. If the input is valid, it creates
        a new amenity and returns the details of the created amenity.
        
        Returns:
            tuple: A response dictionary containing amenity details and status code 201.
            tuple: Error message and status code 400 if input is invalid.
        """
        
        amenity_data = api.payload
        
        if not amenity_data:
            return {'message': 'Invalid input data'}, 400
        
        new_amenity = facade.create_amenity(amenity_data)
        
        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201


    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve a list of all amenities.
        
        This method handles the GET request to retrieve a list of all available
        amenities. It returns an array of dictionaries, each containing amenity details.
        
        Returns:
            list: A list of amenities with their details.
        """
        
        amenities = facade.get_all_amenities()
        
        return [
            {
                'id': amenity.id,
                'name': amenity.name
            } for amenity in amenities
        ]


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """
    Resource for handling operations on a specific amenity identified by amenity_id.
    """


    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get amenity details by ID.
        
        This method handles the GET request to fetch details of a specific amenity
        by its ID. If the amenity exists, its details are returned. Otherwise, an error
        message is returned with a 404 status.
        
        Args:
            amenity_id (str): The ID of the amenity to retrieve.
        
        Returns:
            tuple: A response dictionary containing amenity details and status code 200.
            tuple: Error message and status code 404 if amenity is not found.
        """
        
        amenities_data = facade.get_amenity(amenity_id)
        
        if not amenities_data:
            return {'message': 'Amenity not found'}, 404
        
        return {
            'id': amenities_data.id,
            'name': amenities_data.name
        }, 200


    @api.response(200, 'Amenity successfully deleted')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """
        Delete an amenity.
        
        This method handles the DELETE request to remove an amenity by its ID. If the
        amenity exists and is successfully deleted, a success message is returned.
        Otherwise, an error message with status 404 is returned.
        
        Args:
            amenity_id (str): The ID of the amenity to delete.
        
        Returns:
            tuple: Success message and status code 200.
            tuple: Error message and status code 404 if amenity is not found.
        """
        
        success = facade.delete_amenity(amenity_id)
        
        if success:
            return {'message': 'Amenity deleted successfully'}, 200
        
        else:
            return {'error': 'Amenity not found'}, 404


    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """
        Update an amenity's information.
        
        This method handles the PUT request to update an amenity's information. It expects
        the updated data to match the `amenity_model`. If the input is valid and the amenity exists,
        it updates the amenity and returns a success message. If the amenity is not found, an error
        message is returned with a 404 status.
        
        Args:
            amenity_id (str): The ID of the amenity to update.
        
        Returns:
            tuple: Success message and status code 200 if the update is successful.
            tuple: Error message and status code 404 if amenity is not found.
            tuple: Error message and status code 400 if input data is invalid.
        """
        
        amenity_data = api.payload
        
        if not amenity_data:
            return {'message': 'Invalid input data'}, 400
         
        updated_amenities = facade.update_amenity(amenity_id, amenity_data)
        
        if not updated_amenities:
            return {'message': 'Amenity not found'}, 404
        
        return {"message": "Amenity updated successfully"}, 200