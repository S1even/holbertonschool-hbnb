#!/usr/bin/python3
from .base_model import BaseModel
import uuid

class Amenity(BaseModel):
    
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
    
    def _validate_name(self, name: str) -> str:
        """Validates that the amenity name is not empty and under 50 characters."""
        if not name or len(name) > 50:
            raise ValueError("Amenity name must be non-empty and less than 50 characters.")
        return name
