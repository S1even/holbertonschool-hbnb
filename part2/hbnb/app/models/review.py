#!/usr/bin/python3
from base_model import BaseModel
from place import Place
from user import User


class Review(BaseModel):
    def init(self, text: str, rating: int, place: Place, user: User):
        super().init()
        self.text = text
        self.rating = self._validate_rating(rating)
        self.place = place
        self.user = user

    def _validate_rating(self, rating: int) -> int:
        """Validates the rating is between 1 and 5."""
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return rating
