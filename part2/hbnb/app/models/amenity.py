#!/usr/bin/python3
from base_model import BaseModel


class Amenity(BaseModel):
    def init(self, name: str):
        super().init()
        self.name = self._validate_name(name)

    def _validate_name(self, name: str) -> str:
        """Validates that the amenity name is not empty and under 50 characters."""
        if not name or len(name) > 50:
            raise ValueError("Amenity name must be non-empty and less than 50 characters.")
        return name
