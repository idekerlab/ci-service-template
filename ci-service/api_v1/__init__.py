from flask import Flask
from flask_restful import Api
from utils.logger_factory import LoggerUtil

task_logger = LoggerUtil.get_logger(__name__)

# Shared constants for this API.
API_VERSION = '/v1'

RESULT_TYPE = 'result_type'
RESULT_FILE = 'file'
RESULT_MEMORY = 'memory'

app = Flask(__name__)
logger = app.logger

api = Api(app, prefix=API_VERSION)
