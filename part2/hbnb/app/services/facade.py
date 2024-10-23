import uuid
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()


#---------------------------User---------------------------#


    def create_user(self, user_data):
        User.validate_request_data(user_data)
        user = User(**user_data)
        self.user_repo.add(user)
        return user


    def get_user(self, user_id):
        return self.user_repo.get(user_id)


    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)


    def get_all_users(self):
        return list(self.user_repo.get_all())


    def update_user(self, user_id, user_data):
        User.validate_request_data(user_data)
        obj = self.get_user(user_id)
        if obj:
            obj.update(user_data)
        return obj


    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        if user:
            self.user_repo.delete(user_id)
            return {"message": "User deleted successfully"}


#---------------------------Place---------------------------#


    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place


    def get_place(self, place_id):
        return self.place_repo.get(place_id)


    def get_all_places(self):
        return self.place_repo.get_all()


    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if place:
            if 'title' in place_data:
                place.title = place_data['title']
            if 'description' in place_data:
                place.description = place_data['description']
            if 'price' in place_data:
                place.price = place_data['price']
            if 'latitude' in place_data:
                place.latitude = place_data['latitude']
            if 'longitude' in place_data:
                place.longitude = place_data['longitude']
            if 'owner_id' in place_data:
                place.owner_id = place_data['owner_id']
            self.place_repo.update(place, place_data)
        return place


    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            self.place_repo.delete(place_id)
            return {"message": "Place deleted successfully"}


#---------------------------Amenity---------------------------#


    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity


    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)


    def get_all_amenities(self):
        return self.amenity_repo.get_all()


    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if amenity:
            if 'name' in amenity_data:
                amenity.name = amenity_data['name']
            self.amenity_repo.update(amenity, amenity_data)
        return amenity


    def delete_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            self.amenity_repo.delete(amenity_id)
            return {"message": "Amenity deleted successfully"}


#---------------------------Review---------------------------#


    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review


    def get_review(self, review_id):
        return self.review_repo.get(review_id)


    def get_all_reviews(self):
        return self.review_repo.get_all()


    def get_reviews_by_place(self, place_id):
        return self.review_repo.get(place_id)


    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if review:
            if 'text' in review_data:
                review.text = review_data['text']
            if 'rating' in review_data:
                review.rating = review_data['rating']
            if 'user_id' in review_data:
                review.user_id = review_data['user_id']
            self.review_repo.update(review, review_data)
        return review


    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
            return {'message': 'Review deleted successfully'}