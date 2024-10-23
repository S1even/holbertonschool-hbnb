import uuid
from datetime import datetime


class BaseModel:
    """
    A base model class that provides common attributes and methods for all models.

    Attributes:
        id (str): A unique identifier for the object.
        created_at (datetime): Timestamp when the object was created.
        updated_at (datetime): Timestamp when the object was last updated.
    """


    def __init__(self):
        """
        Initializes a BaseModel instance with a unique ID and timestamps.

        The ID is generated using UUID4, and the timestamps are set to the current datetime.
        """
        
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


    def save(self):
        """
        Update the 'updated_at' timestamp whenever an object is modified.

        This method should be called to refresh the update timestamp whenever
        the object's state is changed.
        """
        
        self.updated_at = datetime.now()


    def update(self, data):
        """
        Update object attributes with a dictionary of new values.

        Args:
            data (dict): A dictionary containing the attributes to update and their new values.
        
        This method checks if the keys in the dictionary correspond to attributes
        of the object and updates them accordingly. After updating the attributes,
        the 'save' method is called to refresh the updated_at timestamp.
        """
        
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()