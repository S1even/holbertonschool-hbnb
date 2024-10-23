import uuid
from datetime import datetime
from .base_model import BaseModel
import re


regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'


class User(BaseModel):
    """
    Represents a user in the application.

    Each user has a first name, last name, email, and can have multiple places associated with them.

    Attributes:
        id (str): A unique identifier for the user.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address.
        is_admin (bool): Indicates if the user is an administrator.
        places (list): A list of places associated with the user.
    """


    def __init__(self, first_name, last_name, email):
        """
        Initializes a User instance.

        Args:
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            email (str): The user's email address.

        Raises:
            ValueError: If any provided attributes are invalid.
        """
        
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = False
        self.places = []


    def save(self):
        """
        Update the 'updated_at' timestamp whenever the user object is modified.
        """
        
        super().save()


    def update(self, data):
        """
        Update the attributes of the user object based on the provided dictionary.

        Args:
            data (dict): A dictionary containing the attributes to be updated.
        """
        
        super().update(data)


    @staticmethod
    def validate_request_data(data: dict):
        """
        Validate the request data for creating or updating a user.

        Args:
            data (dict): A dictionary containing user attributes.

        Raises:
            ValueError: If any of the provided attributes are invalid.

        Returns:
            dict: The validated data if all checks pass.
        """
        
        for key in data.keys():
            value = data[key]
            
            if key == 'first_name' or key == 'last_name':
                if isinstance(value, str) and (len(value) > 50 or len(value) < 1):
                    raise ValueError("String must be less than 50 chars and not empty.")
            
            elif key == 'email':
                if re.match(regex, data["email"]):
                    return data
                else:
                    raise ValueError("Email must follow standard email format.")
            
            elif key == 'id':
                try:
                    uuid_user = uuid.UUID(data[key], version=4)
                except ValueError:
                    raise ValueError("Invalid UUID format for ID.")
        
        return data