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
def teardown():
    """This calls storage.close
    """
    storage.close()
HOST = os.getenv(HBNB_API_HOST)
PORT = os.getenv(HBNB_API_PORT)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True)

