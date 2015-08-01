from flask import Flask
from flask_restful import Api

from apiv1.resource_version import VersionResource
from apiv1.queue.jobs import Jobs
from apiv1.queue.job import SingleJob
from apiv1.queue.result import Result
from apiv1.resource_hello import HelloResource
from apiv1.resource_example_on_memory import MemoryResultExampleResource, \
    GraphAlgorithmResource
from apiv1.resource_return_as_file import FileResultExampleResource

from apiv1.resource_add_one import AddOneResource

from apiv1.resource_community import CommunityDetectionResource
from apiv1.queue.queue import TaskQueue

from apiv1.resource_upload import UploadResource

from apiv1.queue.task import Task

# Shared constants for this API.
API_VERSION = '/v1'

app = Flask(__name__)
logger = app.logger

api = Api(app, prefix=API_VERSION)

# Endpoints

# Top-level URL - simply returns service name
api.add_resource(VersionResource, '')

# Toy example service: Return greeting message.
api.add_resource(AddOneResource, '/addone')
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

########### New Worker Test ################
api.add_resource(CommunityDetectionResource, '/community')

api.add_resource(TaskQueue, '/queue')
api.add_resource(Task, '/queue/<job_id>')

######## File uploader #########
api.add_resource(UploadResource, '/upload')

# Initialization
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
