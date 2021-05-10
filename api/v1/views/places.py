#!/usr/bin/python3
""" This file handles all API actions
"""

from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places_by_city(city_id=None):
    """This gets all the places based on a city id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    place_objs = storage.all(Place).values()
    places_list = []
    for place in place_objs:
        if city_id == place.city_id:
            places_list.append(place.to_dict())
    return jsonify(places_list)
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id=None):
    """gets place obj based on place id
    """
    place_objs = storage.all(Place).values()
    for place in place_objs:
        if place_id == place.id:
            return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ This deletes a place obj
    """
    place_objs = storage.all(Place).values()
    for place in place_objs:
        if place_id == place.id:
            place.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """This creates a place
    """
    obj_dict = request.get_json()

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if obj_dict is None:
        abort(400, 'Not a JSON')
    if "user_id" not in obj_dict:
        abort(400, 'Missing user_id')
    user_id = obj_dict.get("user_id")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if "name" not in obj_dict:
        abort(400, 'Missing name')
    place_obj = Place(**obj_dict)
    place_obj.city_id = city_id
    place_obj.save()
    return jsonify(place_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """This updates a place obj
    """
    place_objs = storage.all(Place).values()
    for place in place_objs:
        if place_id == place.id:
            obj_dict = request.get_json()
            if not obj_dict:
                abort(400, 'Not a JSON')

            forbidden_keys = ['id', 'user_id', 'city_id',
                              'created_at', 'updated_at']
            for key, val in obj_dict.items():
                if key not in forbidden_keys:
                    setattr(place, key, val)
            place.save()
            return jsonify(place.to_dict()), 200
    abort(404)
