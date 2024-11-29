from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.repository import UserRepository
from app import bcrypt


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        """Create a new user with the given data."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """ Retrieve a user by its ID."""
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        """ Retrieve a user by its email."""
        return self.user_repo.get_by_email(email)
    
    def get_all_users(self):
        """ Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, updated_data):
        """ Update an existing user by its ID."""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(updated_data)
        self.user_repo.update(user_id, updated_data)
        return user
    
    def create_amenity(self, amenity_data):
        """Create a new amenity with the given data."""
        if 'name' not in amenity_data or not amenity_data['name']:
            raise ValueError("Amenity name is required")
        
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by its ID"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        return amenity

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity by its ID."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
        
        self.amenity_repo.add(amenity)
        return amenity

    def create_place(self, place_data):
        """ Create a new place with the given data."""
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """ Retrieve a place by its ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """ Retrieve all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """ Update an existing place by its ID."""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        place.update(place_data)
        self.place_repo.update(place_id, place_data)
        return place

    def create_review(self, review_data):
        """ Create a new review with the given data."""
        validated_data = {
            'text': str(review_data.get('text')),
            'rating': int(review_data.get('rating')),
            'place_id': str(review_data.get('place_id')),
            'user_id': str(review_data.get('user_id'))
        }
        new_review = Review(**validated_data)
        self.review_repo.add(new_review)
        return new_review

    def get_all_reviews(self):
        """ Retrieve all reviews."""
        return self.review_repo.get_all()
    
    def get_review(self, review_id):
        """ Retrieve a review by its ID."""
        return self.review_repo.get(review_id)

    def get_reviews_by_place(self, place_id):
        """ Retrieve all reviews for a given place."""
        all_reviews = self.review_repo.get_all()
        reviews_for_place = [review for review in all_reviews if review.place_id == place_id]
        return reviews_for_place

    def update_review(self, review_id, data):
        """ Update an existing review by its ID."""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        review.update(data)
        self.review_repo.add(review)
        return review

    def delete_review(self, review_id):
        """ Delete a review by its ID."""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError('Review not found')
        self.review_repo.delete(review_id)

    def get_review_by_user_and_place(self, user_id, place_id):
        """Check if a user has already reviewed a specific place."""
        all_reviews = self.review_repo.get_all()
        for review in all_reviews:
            if review.user_id == user_id and review.place_id == place_id:
                return review
        return None

    def hash_password(self, password):
        """Hashes the password before storing it."""
        return bcrypt.generate_password_hash(password).decode('utf-8')