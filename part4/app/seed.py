from app import db, bcrypt
from app.models.user import User
from app.models.amenity import Amenity
import uuid


def seed_database():
    """
    This function seeds the database with initial data, including:
    - An admin user (if not already present)
    - A few amenities (if they are not already present)
    """

    if not User.query.filter_by(email='admin@hbnb.io').first():
        admin_password = bcrypt.generate_password_hash('admin1234').decode('utf-8')

        admin_user = User(
            id='36c9050e-ddd3-4c3b-9731-9f487208bbc1',
            email='admin@hbnb.io',
            first_name='Admin',
            last_name='HBnB',
            password=admin_password,
            is_admin=True
        )
        db.session.add(admin_user)

    amenities = [
        {'name': 'WiFi'},
        {'name': 'Swimming Pool'},
        {'name': 'Air Conditioning'}
    ]

    for amenity_data in amenities:
        if not Amenity.query.filter_by(name=amenity_data['name']).first():
            amenity = Amenity(name=amenity_data['name'])
            db.session.add(amenity)

    db.session.commit()