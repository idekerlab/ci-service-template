from flask import Flask
from flask_restful import Api
from api_v1.service_version import Version
from api_v1.jobs import Jobs
from api_v1.job import SingleJob
from api_v1.result import Result
from api_v1.service_hello import HelloService
from api_v1.service_example_memory import MemoryResultServiceExample, GraphAnalysis
from api_v1.service_example_file import FileResultServiceExample

# Shared constants for this API.
API_VERSION = '/v1'

app = Flask(__name__)
logger = app.logger

api = Api(app, prefix=API_VERSION)

# Endpoints

# Top-level URL - simply returns service name
api.add_resource(Version, '')

# Toy example service: Return greeting message.
api.add_resource(HelloService, '/hello')

# Sample services: Calculate graph statistics
api.add_resource(GraphAnalysis, '/algorithms')
api.add_resource(MemoryResultServiceExample, '/algorithms/<algorithm_name>')

# Sample services: Using temp files for results
api.add_resource(FileResultServiceExample, '/generators/scalefree')

# Task Queue
api.add_resource(Jobs, '/jobs')
api.add_resource(SingleJob, '/jobs/<job_id>')
api.add_resource(Result, '/jobs/<job_id>/result')

# Initialization
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
