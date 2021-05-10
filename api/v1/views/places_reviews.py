#!/usr/bin/python3
"""This file retrives an object into a vaild JSON
"""

from models.review import Review
from models.user import User
from models.place import Place
from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_review_place(place_id=None):
    """This gets a review based on the place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    review_objs = storage.all(Review).values()
    review_list = []
    for review in review_objs:
        if place_id == review.place_id:
            review_list.append(review.to_dict())
    return jsonify(review_list)
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id=None):
    """Gets review based on place id
    """
    review_objs = storage.all(Review).values()
    for review in review_objs:
        if review_id == review.id:
            return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id=None):
    """ This deletes a review based on its review id
    """
    review_objs = storage.all(Review).values()
    for review in review_objs:
        if review_id == review.id:
            review.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id=None):
    """This Transforms an HTTP request into json
    """
    obj_dict = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if obj_dict is None:
        abort(400, 'Not a JSON')
    if "user_id" not in obj_dict:
        abort(400, 'Missing user_id')
    user_id = obj_dict.get("user_id")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if "text" not in obj_dict:
        abort(400, 'Missing text')
    review_obj = Review(**obj_dict)
    review_obj.place_id = place_id
    review_obj.save()
    return jsonify(review_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """This updates a review object
    """
    review_objs = storage.all(Review).values()
    for review in review_objs:
        if review_id == review.id:
            obj_dict = request.get_json()
            if not obj_dict:
                abort(400, 'Not a JSON')

            forbidden_keys = ['id', 'user_id', 'place_id', 'created_at',
                              'updated_at']
            for key, val in obj_dict.items():
                if key not in forbidden_keys:
                    setattr(review, key, val)
            review.save()
            return jsonify(review.to_dict()), 200
    abort(404)
