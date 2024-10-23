from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade


api = Namespace('reviews', description='Review operations')


review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


facade = HBnBFacade()


@api.route('/')
class ReviewList(Resource):
    """
    Resource for handling requests to list all reviews and create new reviews.
    """

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new review.

        This method handles the POST request to create a new review for a place.
        It expects input data to match the `review_model` format. If the required
        fields are present and valid, a new review is created and returned.

        Returns:
            tuple: A response dictionary with the review details and status code 201.
            tuple: Error message and status code 400 if input data is invalid.
        """
        
        review_data = api.payload

        if ('text' not in review_data or 'rating' not in review_data or
                'user_id' not in review_data or 'place_id' not in review_data):
            return {'message': 'Missing required fields'}, 400

        new_review = facade.create_review(review_data)
        
        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user_id,
            'place_id': new_review.place_id
        }, 201


    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve a list of all reviews.

        This method handles the GET request to fetch all reviews. It returns a 
        list of reviews with basic details such as review text and rating.

        Returns:
            list: A list of dictionaries containing review details like ID, 
                  text, and rating.
        """
        
        reviews = facade.get_all_reviews()
        
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            } for review in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    """
    Resource for handling operations on a specific review identified by review_id.
    """

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Get review details by ID.

        This method handles the GET request to fetch the details of a specific
        review using the review's ID. If the review exists, its details are returned.
        Otherwise, a 404 error is returned.

        Args:
            review_id (str): The ID of the review to retrieve.

        Returns:
            tuple: A response dictionary containing the review details and status code 200.
            tuple: Error message and status code 404 if the review is not found.
        """
        
        review = facade.get_review(review_id)
        
        if not review:
            return {'error': 'Review not found'}, 404
        
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200


    @api.expect(review_model)
    @api.response(200, 'Review successfully updated')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """
        Update a review's information.

        This method handles the PUT request to update the details of a specific
        review by its ID. It expects input data to match the `review_model` format.
        If the review is found and the input is valid, the review's details are
        updated. Otherwise, an error message is returned.

        Args:
            review_id (str): The ID of the review to update.

        Returns:
            tuple: Success message and status code 200 if the update is successful.
            tuple: Error message and status code 404 if the review is not found.
            tuple: Error message and status code 400 if input data is invalid.
        """
        
        review_data = api.payload

        if not review_data:
            return {'message': 'Invalid input data'}, 400
        
        updated_review = facade.update_review(review_id, review_data)
        
        if not updated_review:
            return {'error': 'Review not found'}, 404
        
        return {"message": "Review updated successfully"}, 200


    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """
        Delete a review.

        This method handles the DELETE request to remove a review by its ID. If
        the review exists and is deleted successfully, a success message is returned.
        Otherwise, an error message with status 404 is returned.

        Args:
            review_id (str): The ID of the review to delete.

        Returns:
            tuple: Success message and status code 200 if deletion is successful.
            tuple: Error message and status code 404 if the review is not found.
        """
        
        success = facade.delete_review(review_id)
        
        if success:
            return {'message': 'Review deleted successfully'}, 200
        
        return {'error': 'Review not found'}, 404


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    """
    Resource for handling requests to list all reviews for a specific place.
    """


    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get all reviews for a specific place.

        This method handles the GET request to fetch all reviews for a given place
        identified by its ID. If the place exists, a list of reviews is returned.
        Otherwise, a 404 error is returned.

        Args:
            place_id (str): The ID of the place to retrieve reviews for.

        Returns:
            list: A list of dictionaries containing review details for the specified place.
            tuple: Error message and status code 404 if the place is not found.
        """
        
        place_reviews = facade.get_reviews_by_place(place_id)
        
        if not place_reviews:
            return {'error': 'Place not found'}, 404
        
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            } for review in place_reviews
        ], 200