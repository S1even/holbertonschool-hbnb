import uuid
from datetime import datetime


class Review:
    """
    Represents a review for a place.

    Each review includes text, a rating, and associations with a user and a place.

    Attributes:
        id (str): A unique identifier for the review.
        text (str): The text content of the review.
        rating (int): The rating given to the place (between 0 and 5).
        place_id (str): The ID of the place being reviewed.
        user_id (str): The ID of the user who wrote the review.
        created_at (datetime): The timestamp when the review was created.
        updated_at (datetime): The timestamp when the review was last updated.
    """


    def __init__(self, text, rating, place_id, user_id, id=None):
        """
        Initializes a Review instance.

        Args:
            text (str): The text content of the review.
            rating (int): The rating given to the place (must be between 0 and 5).
            place_id (str): The ID of the place being reviewed.
            user_id (str): The ID of the user writing the review.
            id (str, optional): A unique identifier for the review. If not provided, a new UUID is generated.

        Raises:
            ValueError: If the text is empty, the rating is not between 0 and 5, or the IDs are not strings.
        """
        
        if not text:
            raise ValueError("Review text is required")
        self.text = text

        if rating < 0 or rating > 5:
            raise ValueError("Rating must be between 0 and 5")
        self.rating = rating

        if not isinstance(place_id, str):
            raise ValueError("Invalid Place ID")
        self.place_id = place_id

        if not isinstance(user_id, str):
            raise ValueError("Invalid User ID")
        self.user_id = user_id

        self.id = id or str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


    def save(self):
        """
        Update the 'updated_at' timestamp whenever the review is modified.
        """
        
        self.updated_at = datetime.now()


    def dict(self):
        """
        Convert the review instance into a dictionary format.

        Returns:
            dict: A dictionary representation of the review, including its attributes.
        """
        
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }