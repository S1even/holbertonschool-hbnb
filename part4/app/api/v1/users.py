"""
User API module for managing user resources.

Endpoints:
    - /users/: Retrieve all users or create a new user.
    - /users/<user_id>: Retrieve, update, or delete a specific user.
"""


from flask_restx import Namespace, Resource, fields
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade


api = Namespace('users', description='User operations')


user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
})


update_user_model = api.model('UpdateUser', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
})


facade = HBnBFacade()
user_email = User()


@api.route('/')
class UserList(Resource):
    """
    Resource class for managing user collections.

    Methods:
        get: Retrieve all users.
        post: Create a new user.
    """


    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """
        Retrieve all users.

        Returns:
            list: A list of user details.
            HTTP Status: 200.
        """

        users = facade.get_all_users()

        return [
            {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}
            for user in users
        ], 200


    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid email format')
    def post(self):
        """
        Create a new user.

        Requires a valid JWT token. Ensures that email is unique and correctly formatted.

        Returns:
            dict: Details of the created user.
            HTTP Status: 201 if successful, 400 otherwise.
        """

        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])

        if existing_user:
            return {'error': 'Email already registered'}, 400

        if not user_email.validate_email(user_data['email']):
            return {"error": "Invalid email format"}, 400

        user_data['password'] = facade.hash_password(user_data['password'])

        new_user = facade.create_user(user_data)

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201


@api.route('/<user_id>')
class UserResource(Resource):
    """
    Resource class for managing a single user.

    Methods:
        get: Retrieve user details.
        put: Update user details.
    """


    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Retrieve details of a specific user.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            dict: Details of the user.
            HTTP Status: 200 if successful, 404 if not found.
        """

        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404
        
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200


    @jwt_required()
    @api.expect(update_user_model)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """
        Update details of a specific user.

        Requires a valid JWT token. Only the user themselves or an admin can update user details. 
        Regular users cannot modify email or password.

        Args:
            user_id (str): The ID of the user to update.

        Returns:
            dict: Updated details of the user.
            HTTP Status: 200 if successful, 400, 403, or 404 otherwise.
        """

        current_user = get_jwt_identity()

        data = api.payload

        if current_user.get('is_admin'):
            if 'email' in data:
                existing_user = facade.get_user_by_email(data['email'])
                if existing_user and str(existing_user.id) != user_id:
                    return {'message': 'Email already in use'}, 400

            if 'password' in data:
                data['password'] = facade.hash_password(data['password'])

        else:
            if current_user.get('id') != user_id:
                return {'message': 'Unauthorized action'}, 403

            if 'email' in data or 'password' in data:
                return {'message': 'You cannot modify email or password'}, 400

        try:
            updated_user = facade.update_user(user_id, data)
            if not updated_user:
                return {'message': 'User not found'}, 404

            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200

        except ValueError as e:
            return {'message': str(e)}, 400