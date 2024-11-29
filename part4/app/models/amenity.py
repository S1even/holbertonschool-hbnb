from app import db
from uuid import uuid4

class Amenity(db.Model):
    __tablename__ = 'amenities'

    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, **kwargs):
        super(Amenity, self).__init__(**kwargs)
        if 'id' not in kwargs:
            self.id = str(uuid4())