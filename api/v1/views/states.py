#!/usr/bin/python3
"""This file retrives an object into a vaild JSON
"""

from models.state import State
from models import storage
from flask import Flask, abort, jsonify, request


@app_views.route('/states/<state_id>')
def states(state_id):
    """Gets state object
    """
    obj = storage.all()
    for id in obj:
        if state_id == id:
            State.to_dict()
        else:
            abort(404)


@app_views.route('/states/<state_id>')
def del_state(state_id):
    """ This deletes a state object
    """
    obj = storage.all()
    for id in obj:
        if state_id == id:
            State.delete()
        else:
            return jsonify({}), 200


@app_views.route('/states')
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


@app_views.route('/states/<state_id>')
def put_state(state_id):
    obj_dict = request.get_json()

    if obj_dict is None:
        abort(400, 'Not a JSON')
    else:
        for key in obj_dict:
            if obj_dict[key] == state_id:
                storage_obj = storage.all(State)
    return jsonify(storage_obj), 200
