from flask import Flask
from flask_restful import Api
from api_v1.resource_version import VersionResource
from api_v1.jobs import Jobs
from api_v1.job import SingleJob
from api_v1.result import Result
from api_v1.resource_hello import HelloResource
from api_v1.resource_example_on_memory import MemoryResultExampleResource, GraphAlgorithmResource
from api_v1.resource_return_as_file import FileResultExampleResource

# Shared constants for this API.
API_VERSION = '/v1'

app = Flask(__name__)
logger = app.logger

api = Api(app, prefix=API_VERSION)

# Endpoints

# Top-level URL - simply returns service name
api.add_resource(VersionResource, '')

# Toy example service: Return greeting message.
api.add_resource(HelloResource, '/hello')

# Sample services: Calculate graph statistics
api.add_resource(GraphAlgorithmResource, '/algorithms')
api.add_resource(MemoryResultExampleResource, '/algorithms/<algorithm_name>')

# Sample services: Using temp files for results
api.add_resource(FileResultExampleResource, '/generators/scalefree')

# Task Queue
api.add_resource(Jobs, '/jobs')
api.add_resource(SingleJob, '/jobs/<job_id>')
api.add_resource(Result, '/jobs/<job_id>/result')

# Initialization
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
