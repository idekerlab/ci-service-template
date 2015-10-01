import logging

from flask import Flask
from flask_restful import Api

from apiv1.queue.task_result import TaskResult
from apiv1.resource_version import VersionResource
from apiv1.queue.queue import TaskQueue
from apiv1.resource_upload import UploadResource
from apiv1.queue.task import Task
from apiv1.resource_service import ServiceResource
from apiv1.resource_services import ServicesResource

API_VERSION = '/v1'

app = Flask(__name__)
api = Api(app, prefix=API_VERSION)

# Show API version
api.add_resource(VersionResource, '')


# Service list
api.add_resource(ServicesResource, '/services')

# Endpoint to send actual jobs to a service
api.add_resource(ServiceResource, '/services/<string:name>')

# Job list
api.add_resource(TaskQueue, '/queue')

# Status of a job
api.add_resource(Task, '/queue/<job_id>')

# Result of the job
api.add_resource(TaskResult, '/queue/<job_id>/result')

# Upload/Download data from a file server
api.add_resource(UploadResource, '/upload')


# Initialization
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
    logging.debug('Submit agent REST API server is ready')
