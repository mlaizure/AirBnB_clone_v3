#!/usr/bin/python3
""" This file handles all API actions
"""

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, json, jsonify, request


@app_views.route('/users', strict_slashes=False)
@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """This gets the user Object from the main
    """
    user_objs = storage.all(User).values()
    if not user_id:
        user_list = []
        for user in user_objs:
            user_list.append(user.to_dict())
        return jsonify(user_list)

    for user in user_objs:
        if user_id == user.id:
            return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods-['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """This gets the user Object based on the id and deletes it
    """
    user_object = storage.all(User).values()

    for user in user_object:
        if user_id == user.id:
            user.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ This creates a HTTP body response into
    a message that a dictionary
    """
    user_object = request.get_json()

    if user_object is None:
        abort(400, 'Not a JSON')
    if 'email' not in user_object:
        abort(400, 'Missing email')
    if 'password' not in user_object:
        abort(400, 'Missing password')
    else:
        user_dict = User(**user_object)
        user_dict.save()
        return jsonify(user_dict.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """This ubdates the user object
    """
    user_objs = storage.all(User).values()
    for user in user_objs:
        if user_id == user.id:
            user_json = request.get_json()
            if not user_json:
                abort(400, 'Not a JSON')

            forbidden_keys = ['id', 'email', 'created_at', 'updated_at']

            for key, val in user_json.items():
                if key not in forbidden_keys:
                    setattr(user, key, val)
            user.save()
            return jsonify(user.to_dict()), 200

    abort(404)
