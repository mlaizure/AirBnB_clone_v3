#!/usr/bin/python3
"""This file retrives an object into a vaild JSON
"""

from models import amenity
from models.amenity import Amenity
from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id=None):
    """Gets amenity object
    """
    amenity_objs = storage.all(Amenity).values()
    if not amenity_id:
        amenity_list = []
        for amenity in amenity_objs:
            amenity_list.append(amenity.to_dict())
        return jsonify(amenity_list)

    for amenity in amenity_objs:
        if amenity_id == amenity.id:
            return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """ This deletes a amenity object
    """
    amenity_objs = storage.all(Amenity).values()
    for amenity in amenity_objs:
        if amenity_id == amenity.id:
            amenity.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """This creates a HTTP body response
        into a message that a dictonary
    """
    obj_dict = request.get_json()

    if obj_dict is None:
        abort(400, 'Not a JSON')
    if "name" not in obj_dict:
        abort(400, 'Missing name')
    else:
        amenity_obj = Amenity(**obj_dict)
        amenity_obj.save()
        return jsonify(amenity_obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """This updates a amenity obj
    """
    amenity_objs = storage.all(Amenity).values()
    for amenity in amenity_objs:
        if amenity_id == amenity.id:
            obj_dict = request.get_json()
            if not obj_dict:
                abort(400, 'Not a JSON')

            forbidden_keys = ['id', 'created_at', 'updated_at']
            for key, val in obj_dict.items():
                if key not in forbidden_keys:
                    setattr(amenity, key, val)
            amenity.save()
            return jsonify(amenity.to_dict()), 200
    abort(404)
