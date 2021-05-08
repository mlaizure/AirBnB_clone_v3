#!/usr/bin/python3
""" This function sets route for /status
"""

from api.v1.views import app_views
from flask import app, jsonify
from models import storage
from models import review
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """This returns a JSON status
    """
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def count():
    """ It returns the count for each object in DB
    """
    count_dict = {}
    count_dict["amenities"] = storage.count(Amenity)
    count_dict["cities"] = storage.count(City)
    count_dict["places"] = storage.count(Place)
    count_dict["reviews"] = storage.count(Review)
    count_dict["users"] = storage.count(User)
    count_dict["states"] = storage.count(State)

    return count_dict
