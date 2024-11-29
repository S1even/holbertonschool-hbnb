from app import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    """
    A base model to include common fields and methods for other models.

    Attributes:
        id (str): Unique identifier for the record, generated as a UUID4 string.
        created_at (datetime): Timestamp when the record was created.
        updated_at (datetime): Timestamp when the record was last updated.

    Methods:
        save: Updates the `updated_at` field and commits the record to the database.
        update: Updates the model instance with a dictionary of values and saves it.
    """

    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


    def save(self):
        """
        Saves the model instance to the database.
        Updates the `updated_at` field to the current time before committing.
        """

        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()


    def update(self, data):
        """
        Updates the model instance with key-value pairs from a dictionary.

        Args:
            data (dict): A dictionary of attributes to update the model instance.

        Raises:
            AttributeError: If any of the keys in `data` do not correspond to an attribute of the model.
        """

        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

            else:
                raise AttributeError(f"Attribute {key} not found on {self.__class__.__name__}.")

            self.save()