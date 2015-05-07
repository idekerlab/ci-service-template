from flask import Flask
from flask_restful import Api

# Shared constants for this API.
API_VERSION = '/v1'

app = Flask(__name__)
logger = app.logger

api = Api(app, prefix=API_VERSION)