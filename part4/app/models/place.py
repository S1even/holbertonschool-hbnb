from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.models.base_model import BaseModel

class Place(BaseModel):
    __tablename__ = 'places'

    _title = db.Column(db.String(255), nullable=False)
    _description = db.Column(db.Text, nullable=True)
    _price = db.Column(db.Numeric(10, 2), nullable=False)
    _latitude = db.Column(db.Float, nullable=False)
    _longitude = db.Column(db.Float, nullable=False)
    _owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    @hybrid_property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or len(value) > 255:
            raise ValueError(
                'Title must a maximum length of 255 characters.'
            )
        self._title = value

    @hybrid_property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value and not isinstance(value, str) or len(value) > 2048:
            raise ValueError(
                'Description must be a string with a\
                 maximum length of 2048 characters.'
            )
        self._description = value

    @hybrid_property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(
                'Price must be a positive number.'
            )
        self._price = value

    @hybrid_property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90.0 <= value <= 90.0):
            raise ValueError(
                'Latitude must be a number between -90.0 and 90.0.'
            )
        self._latitude = value

    @hybrid_property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(
                'Longitude must be a number between -180.0 and 180.0.'
            )
        elif not (-180.0 <= value <= 180.0):
            raise ValueError(
                'Longitude must be a number between -180.0 and 180.0.'
            )
        self._longitude = value

    @hybrid_property
    def owner_id(self):
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        if not isinstance(value, str) or len(value) != 36:
            raise ValueError(
                'Owner ID must be a string of 36 characters.'
            )
        self._owner_id = value