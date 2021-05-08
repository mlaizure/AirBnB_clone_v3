#!/usr/bin/python3
"""This file retrives an object into a vaild JSON
"""

from models.city import City
from models.state import State
from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_by_state(state_id=None):
    """gets list of cities based on state id
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    city_objs = storage.all(City).values()
    cities_list = []
    for city in city_objs:
        if state_id == city.state_id:
            cities_list.append(city.to_dict())
        return jsonify(cities_list)
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id=None):
    """gets city obj based on city id
    """
    city_objs = storage.all(City).values()
    for city in city_objs:
        if city_id == city.id:
            return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """ This deletes a city obj
    """
    city_objs = storage.all(City).values()
    for city in city_objs:
        if city_id == city.id:
            city.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """This creates a city
    """
    obj_dict = request.get_json()

    if obj_dict is None:
        abort(400, 'Not a JSON')
    if "name" not in obj_dict:
        abort(400, 'Missing name')
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city_obj = City(**obj_dict)
    city_obj.state_id = state_id
    city_obj.save()
    return jsonify(city_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """This updates a city obj
    """
    city_objs = storage.all(City).values()
    for city in city_objs:
        if city_id == city.id:
            obj_dict = request.get_json()
            if not obj_dict:
                abort(400, 'Not a JSON')

            forbidden_keys = ['id', 'state_id', 'created_at', 'updated_at']
            for key, val in obj_dict.items():
                if key not in forbidden_keys:
                    setattr(city, key, val)
            city.save()
            return jsonify(city.to_dict()), 200
    abort(404)
