from flask import Flask
from flask_restful import Api

from utils.logger_factory import LoggerUtil

# Shared constants for this API.
API_VERSION = '/v1'

app = Flask(__name__)
logger = app.logger

task_logger = LoggerUtil.get_logger(__name__)

api = Api(app, prefix=API_VERSION)
