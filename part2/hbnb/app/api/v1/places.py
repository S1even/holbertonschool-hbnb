from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade


api = Namespace('places', description='Place operations')


amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})


user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})


review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})


place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


facade = HBnBFacade()


@api.route('/')
class PlaceList(Resource):
    """
    Resource for handling requests to list all places and create new places.
    """

    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new place.
        
        This method handles the POST request to create a new place. It expects
        the input to match the `place_model` format. If the input is valid, it 
        creates a new place and returns the details of the newly created place.
        
        Returns:
            tuple: A response dictionary with the place details and status code 201.
            tuple: Error message and status code 400 if input data is invalid.
        """
        
        place_data = api.payload
        
        if not place_data:
            return {'message': 'Invalid input data'}, 400
        
        new_place = facade.create_place(place_data)
        
        return {
            "id": new_place.id,
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "owner_id": new_place.owner_id
        }, 201
        

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve a list of all places.
        
        This method handles the GET request to retrieve all available places.
        It returns a list of dictionaries with basic place details (ID, title, 
        latitude, longitude).
        
        Returns:
            list: A list of place dictionaries with details such as ID, title, 
                  latitude, and longitude.
        """
        
        places = facade.get_all_places()
        
        return [
            {
                "id": place.id,
                "title": place.title,
                "latitude": place.latitude,
                "longitude": place.longitude,
            } for place in places
        ]


@api.route('/<place_id>')
class PlaceResource(Resource):
    """
    Resource for handling operations on a specific place identified by place_id.
    """

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get place details by ID.
        
        This method handles the GET request to fetch the details of a specific
        place using the place's ID. If the place exists, its details are returned.
        If not, a 404 error is returned.
        
        Args:
            place_id (str): The ID of the place to retrieve.
        
        Returns:
            tuple: A response dictionary containing the place details and status code 200.
            tuple: Error message and status code 404 if the place is not found.
        """
        
        places_data = facade.get_place(place_id)
        
        if not places_data:
            return {'message': 'Place not found'}, 404
        
        return {
            "id": places_data.id,
            "title": places_data.title,
            "description": places_data.description,
            "price": places_data.price,
            "latitude": places_data.latitude,
            "longitude": places_data.longitude,
            "owner_id": places_data.owner_id
        }, 200


    @api.response(200, 'Place successfully deleted')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """
        Delete a place.
        
        This method handles the DELETE request to remove a place by its ID. If 
        the place exists and is deleted successfully, a success message is returned.
        Otherwise, an error message with status 404 is returned.
        
        Args:
            place_id (str): The ID of the place to delete.
        
        Returns:
            tuple: Success message and status code 200 if deletion is successful.
            tuple: Error message and status code 404 if the place is not found.
        """
        
        success = facade.delete_place(place_id)
        
        if success:
            return {'message': 'Place deleted successfully'}, 200
        else:
            return {'error': 'Place not found'}, 404


    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """
        Update a place's information.
        
        This method handles the PUT request to update the details of a specific
        place by its ID. It expects the input to match the `place_model` format.
        If the place is found and the input is valid, the place's details are 
        updated. Otherwise, an error message is returned.
        
        Args:
            place_id (str): The ID of the place to update.
        
        Returns:
            tuple: Updated place details and status code 200 if the update is successful.
            tuple: Error message and status code 404 if the place is not found.
            tuple: Error message and status code 400 if input data is invalid.
        """
        
        place_data = api.payload
        
        if not place_data:
            return {'message': 'Invalid input data'}, 400
    
        updated_place = facade.update_place(place_id, place_data)
        
        if not updated_place:
            return {'message': 'Place not found'}, 404
        
        return {
            "title": updated_place.title,
            "description": updated_place.description,
            "price": updated_place.price,
            "latitude": updated_place.latitude,
            "longitude": updated_place.longitude,
            "owner_id": updated_place.owner_id
        }, 200