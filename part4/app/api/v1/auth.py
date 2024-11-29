"""
This module defines the authentication-related API endpoints for user login using Flask-RESTx.

Endpoints:
    - /auth/login: Authenticates a user and returns a JWT token.
"""


from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import HBnBFacade


api = Namespace('auth', description='Authentication operations')


login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


facade = HBnBFacade()


@api.route('/login')
class Login(Resource):
    """
    Resource class for user login and JWT token generation.

    Methods:
        post: Authenticate a user and return a JWT token.
    """


    @api.expect(login_model)
    def post(self):
        """
        Authenticate a user and return a JWT token.

        This endpoint checks the provided email and password, verifies the credentials,
        and generates a JWT token upon successful authentication.

        Returns:
            dict: A dictionary containing the access token.
            HTTP Status: 200 if authentication is successful, 401 if credentials are invalid.
        """

        credentials = api.payload

        user = facade.get_user_by_email(credentials['email'])

        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(
            identity=str(user.id), 
            additional_claims={'is_admin': user.is_admin} 
        )
        
        return {'access_token': access_token}, 200