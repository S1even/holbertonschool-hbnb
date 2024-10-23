import uuid
from datetime import datetime
from app.models.base_model import BaseModel


class Place(BaseModel):
    """
    Represents a place available for booking.

    Inherits from BaseModel and includes attributes for title, description,
    price, coordinates, owner ID, reviews, amenities, and users.

    Attributes:
        id (str): A unique identifier for the place.
        title (str): The title of the place.
        description (str): A brief description of the place.
        price (float): The price per night for booking the place.
        latitude (float): The latitude coordinate of the place.
        longitude (float): The longitude coordinate of the place.
        owner_id (str): The ID of the owner of the place.
        reviews (list): A list of reviews associated with the place.
        amenities (list): A list of amenities available at the place.
        users (list): A list of users associated with the place.
    """


    def __init__(self, title, description, price, latitude, longitude, owner_id: str, id=None, amenities=[]):
        """
        Initializes a Place instance.

        Args:
            title (str): The title of the place.
            description (str): A description of the place.
            price (float): The price per night for the place.
            latitude (float): The latitude coordinate of the place.
            longitude (float): The longitude coordinate of the place.
            owner_id (str): The ID of the owner of the place.
            id (str, optional): A unique identifier for the place. If not provided, a new UUID is generated.
            amenities (list, optional): A list of amenities associated with the place.
        """
        
        super().__init__()
        self.id = id or str(uuid.uuid4())
        self._title = title
        self._description = description
        self._price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = amenities
        self.users = []


    @property
    def title(self):
        """
        str: The title of the place.
        """
        
        return self._title


    @title.setter
    def title(self, value):
        """
        Set the title of the place.

        Args:
            value (str): The title to set.

        Raises:
            TypeError: If the title exceeds 100 characters.
        """
        
        if len(value) > 100:
            raise TypeError("Error: title is invalid")
        
        self._title = value


    @property
    def description(self):
        """
        str: The description of the place.
        """
        
        return self._description


    @description.setter
    def description(self, value):
        """
        Set the description of the place.

        Args:
            value (str): The description to set.
        """
        
        self._description = value


    @property
    def price(self):
        """
        float: The price per night for the place.
        """
        
        return self._price


    @price.setter
    def price(self, value):
        """
        Set the price for the place.

        Args:
            value (float): The price to set.

        Raises:
            ValueError: If the price is negative.
        """
        
        if value < 0:
            raise ValueError("Price can't be negative")
        self._price = value


    def set_coordinates(self, latitude, longitude):
        """
        Set the latitude and longitude of the place.

        Args:
            latitude (float): The latitude of the place.
            longitude (float): The longitude of the place.

        Raises:
            ValueError: If the coordinates are out of valid range.
        """
        
        if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
            raise ValueError("Coordinates of latitude and longitude aren't correct")
        
        self.latitude = latitude
        self.longitude = longitude


    def add_review(self, review):
        """
        Add a review to the place.

        Args:
            review: The review object to add to the place.
        """
        
        self.reviews.append(review)


    def add_amenity(self, amenity):
        """
        Add an amenity to the place.

        Args:
            amenity: The amenity object to add to the place.
        """
        
        self.amenities.append(amenity)


    def add_user(self, user):
        """
        Add a user to the place.

        Args:
            user: The user object to associate with the place.
        """
        
        self.users.append(user)