#!/usr/bin/python3
""" This function sets route for /status
"""

from api.v1.views import app_views
from flask import app, jsonify

@app_views.route('/status')
def status():
    """This returns a JSON status
    """
    return jsonify(status='OK')
