from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade


api = Namespace('users', description='User operations')


user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')  
})


facade = HBnBFacade()


@api.route('/')
class UserList(Resource):
    """
    Resource for handling requests to list all users and create new users.
    """

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new user.

        This method handles the POST request to create a new user. It expects input
        data to match the `user_model` format. If the user already exists or input 
        data is invalid, an error is returned. Otherwise, a new user is created 
        and returned.

        Returns:
            tuple: A response dictionary with the user's details and status code 201.
            tuple: Error message and status code 400 if email is already registered or 
                   input data is invalid.
        """
        
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as error:
            return {'error': 'Invalid input Data'}, 400
        
        return {
            'id': new_user.id, 
            'first_name': new_user.first_name, 
            'last_name': new_user.last_name, 
            'email': new_user.email
        }, 201

    
    @api.response(200, 'User list retrieved successfully')
    def get(self):
        """
        Retrieve a list of all users.

        This method handles the GET request to fetch all users. It returns a list
        of users with basic details such as first name, last name, and email.

        Returns:
            list: A list of dictionaries containing user details.
        """
        
        users = facade.get_all_users()
        
        return [
            {
                'id': user.id, 
                'first_name': user.first_name, 
                'last_name': user.last_name, 
                'email': user.email
            } for user in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    """
    Resource for handling operations on a specific user identified by user_id.
    """

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Get user details by ID.

        This method handles the GET request to fetch the details of a specific 
        user using their user_id. If the user exists, their details are returned.
        Otherwise, a 404 error is returned.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            tuple: A response dictionary containing the user's details and status code 200.
            tuple: Error message and status code 404 if the user is not found.
        """
        
        user = facade.get_user(user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        return {
            'id': user_id, 
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'email': user.email
        }, 200


    @api.response(200, 'User successfully deleted')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """
        Delete a user.

        This method handles the DELETE request to remove a user by their ID. 
        If the user exists and is successfully deleted, a success message is returned.
        Otherwise, a 404 error is returned.

        Args:
            user_id (str): The ID of the user to delete.

        Returns:
            tuple: Success message and status code 200 if the deletion is successful.
            tuple: Error message and status code 404 if the user is not found.
        """
        
        success = facade.delete_user(user_id)
        
        if success:
            return {'message': 'User deleted successfully'}, 200
        
        return {'error': 'User not found'}, 404


    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """
        Update a user's information.

        This method handles the PUT request to update the details of a specific
        user by their ID. It expects input data to match the `user_model` format.
        If the user is found and the input is valid, the user's details are updated.
        Otherwise, an error message is returned.

        Args:
            user_id (str): The ID of the user to update.

        Returns:
            tuple: A response dictionary containing the updated user's details and status code 200.
            tuple: Error message and status code 404 if the user is not found.
            tuple: Error message and status code 400 if input data is invalid.
        """
        
        updated_data = api.payload
        
        user = facade.update_user(user_id, updated_data)
        
        if not user:
            return {"error": "User not found"}, 404
        
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email 
        }, 200