from app.models.base_model import BaseModel
from app import db


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)


    @classmethod
    def create(cls, text, rating, place_id, user_id):
        """
        Factory method to create a new review instance.
        Validates the text and rating before creating the review.

        Args:
            text (str): The review content.
            rating (int): Rating of the place (1-5).
            place_id (str): ID of the place being reviewed.
            user_id (str): ID of the user leaving the review.

        Returns:
            Review instance.
        """

        validated_text = cls.validate_text(text)
        validated_rating = cls.validate_rating(rating)

        return cls(text=validated_text, rating=validated_rating, place_id=place_id, user_id=user_id)


    @staticmethod
    def validate_text(text):
        """
        Validate that the review text is not empty.
        
        Args:
            text (str): The review text.

        Returns:
            str: The validated text.

        Raises:
            ValueError: If the text is empty.
        """

        if text == "":
            raise ValueError("Review text must be provided.")

        return text


    @staticmethod
    def validate_rating(rating):
        """
        Validate that the rating is between 1 and 5.

        Args:
            rating (int): Rating of the place.

        Returns:
            int: The validated rating.

        Raises:
            ValueError: If the rating is outside the 1-5 range.
        """

        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")

        return rating