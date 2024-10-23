import uuid
from .base_model import BaseModel
from datetime import datetime


class Amenity:
    """
    Represents an amenity with a unique identifier, name, and timestamps.

    Attributes:
        id (str): A unique identifier for the amenity.
        name (str): The name of the amenity.
        created_at (datetime): Timestamp when the amenity was created.
        updated_at (datetime): Timestamp when the amenity was last updated.
    """


    def __init__(self, name):
        """
        Initializes an Amenity instance.

        Args:
            name (str): The name of the amenity. Must be a non-empty string with a maximum length of 50 characters.

        Raises:
            ValueError: If the name is empty or exceeds 50 characters.
        """
        
        if not name or len(name) > 50:
            raise ValueError("Amenity name is required and must be at most 50 characters long.")

        self.name = name
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


    def save(self):
        """
        Updates the updated_at timestamp to the current time.

        This method should be called whenever the amenity is modified to keep track of the last update time.
        """
        
        self.updated_at = datetime.now()


    def dict(self):
        """
        Converts the Amenity instance to a dictionary format.

        Returns:
            dict: A dictionary representation of the amenity, including its ID, name, and timestamps.
        """
        
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }