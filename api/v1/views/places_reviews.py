#!/usr/bin/python3
"""This file retrives an object into a vaild JSON
"""

from models.review import Review
import json
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

    place_objs = storage.all(Place).values()
    place_list = []
    for item in place_objs:
        if place_id == item.id:
            place_list.append(item.to_dict())
    return jsonify(place_list)
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
    if place_id not in obj_dict:
        abort(404)
    if obj_dict is None:
        abort(400, 'Not a JSON')
    if "user_id" not in obj_dict:
        abort(400, 'Missing user_id')
    if "text" not in obj_dict:
        abort(400, 'Missing text')
    place = storage.get(User, json.get('user_id'))
    if not place:
        abort(404)
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
