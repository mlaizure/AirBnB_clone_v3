#!/usr/bin/python3
""" Basic flask application
"""

from flask import Flask, blueprints
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(self):
    """This calls storage.close
    """
    storage.close()

HOST = os.environ.get('HBNB_API_HOST')
if not HOST:
    HOST = '0.0.0.0'
PORT = os.environ.get('HBNB_API_PORT')
if not PORT:
    PORT = '5000'

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True)
