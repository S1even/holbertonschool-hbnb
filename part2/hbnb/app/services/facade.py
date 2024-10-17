from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity
from app.models.user import User

class HBnBFacade:
    
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
    
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        return self.user_repo.get_all()
    
    def create_amenity(self, amenity_data):
        # Logic to create a new amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity
    
    def get_amenity(self, amenity_id):
        # Logic to retrieve a specific amenity by ID
        return self.amenity_repo.get_by_id(amenity_id)
    
    def get_all_amenities(self):
        # Logic to retrieve all amenities
        return self.amenity_repo.get_all()
    
    def update_amenity(self, amenity_id, amenity_data):
        # Logic to update an existing amenity
        amenity = self.amenity_repo.get_by_id(amenity_id)
        if amenity:
            updated_data = {'name': amenity_data.get('name', amenity.name)}
            self.amenity_repo.update(amenity_id, amenity_data)
            return amenity
        return None
