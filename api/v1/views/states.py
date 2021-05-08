#!/usr/bin/python3
"""This file retrives an object into a vaild JSON
"""

from models.state import State
from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<state_id>', strict_slashes=False)
def states(state_id=None):
    """Gets state object
    """
    state_objs = storage.all(State).values()
    if not state_id:
        states_list = []
        for state in state_objs:
            states_list.append(state.to_dict())
        return jsonify(states_list)

    for state in state_objs:
        if state_id == state.id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """ This deletes a state object
    """
    state_objs = storage.all(State).values()
    for state in state_objs:
        if state_id == state.id:
            state.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """This creates a HTTP body response
        into a message that a dictonary
    """
    obj_dict = request.get_json()

    if obj_dict is None:
        abort(400, 'Not a JSON')
    if "name" not in obj_dict:
        abort(400, 'Missing name')
    else:
        state_obj = State(**obj_dict)
        state_obj.save()
        return jsonify(state_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """This updates a state obj
    """
    state_objs = storage.all(State).values()
    for state in state_objs:
        if state_id == state.id:
            obj_dict = request.get_json()
            if not obj_dict:
                abort(400, 'Not a JSON')

            forbidden_keys = ['id', 'created_at', 'updated_at']
            for key, val in obj_dict.items():
                if key not in forbidden_keys:
                    setattr(state, key, val)
            state.save()
            return jsonify(state.to_dict()), 200
    abort(404)
