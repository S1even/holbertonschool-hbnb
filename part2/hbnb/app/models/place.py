#!/usr/bin/python3
from base_model import BaseModel
from user import User


class Place(BaseModel):
    def init(self, title: str, description: str, price: float, latitude: float, longitude: float, owner: User):
        super().init()
        self.title = self._validate_title(title)
        self.description = description
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def _validate_title(self, title: str) -> str:
        """Validates the title of the place."""
        if not title or len(title) > 100:
            raise ValueError("Title must be non-empty and less than 100 characters.")
        return title

    def _validate_price(self, price: float) -> float:
        """Validates that the price is positive."""
        if price <= 0:
            raise ValueError("Price must be a positive value.")
        return price

    def _validate_latitude(self, latitude: float) -> float:
        """Validates the latitude is within valid range."""
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        return latitude

    def _validate_longitude(self, longitude: float) -> float:
        """Validates the longitude is within valid range."""
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        return longitude

    def add_review(self, review):
        """Adds a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Adds an amenity to the place."""
        self.amenities.append(amenity)
