#!/usr/bin/python3
""" Basic flask application
"""

from flask import Flask, blueprints, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
cors = CORS(app, origins='0.0.0.0')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """This calls storage.close
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(self):
    """ This is an error handler that returns a JSON
        formated 404 status code
    """
    return jsonify(error='Not found'), 404

HOST = os.environ.get('HBNB_API_HOST')
if not HOST:
    HOST = '0.0.0.0'
PORT = os.environ.get('HBNB_API_PORT')
if not PORT:
    PORT = '5000'

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True)
