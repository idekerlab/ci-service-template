import uuid
import zmq
import logging

from flask import request
import requests as client

from .resource_base import BaseResource
from .utils.file_util import FileUtil

ROUTER_PORT = 5556
STATUS_PORT = 6666

INPUT_DATA_SERVER_LOCATION = 'http://dataserver:3000/'

logging.basicConfig(level=logging.DEBUG)


class CommunityDetectionResource(BaseResource):
    """
    Sample API for calling new worker pool
    """

    def __init__(self):
        super(CommunityDetectionResource, self).__init__()
        # Data producer to send tasks to workers.
        context = zmq.Context()

        # For pushing tasks to workers
        self.__sender = context.socket(zmq.PUSH)
        self.__sender.bind('tcp://*:' + str(ROUTER_PORT))

        self.__monitor = context.socket(zmq.PUSH)
        self.__monitor.connect('tcp://collector:6666')

    def get(self):
        """
        Simply return description of this service

        :return:
        """
        description = {
            'message': 'Use POST method to submit your graph data.'
        }

        return description, 200

    def post(self):
        """
        POST network data to queue

        :return:
        """
        logging.debug('POST: Task')

        req = client.post(INPUT_DATA_SERVER_LOCATION + 'data', json=request.stream.read(),
                          stream=True)
        logging.debug('File server response Data = ' + str(req.json()))
        file_id = req.json()['fileId']
        # self.parse_args()
        # data = self.parser.parse_args()
        # logging.debug('Original Data = ' + str(data))

        job_id = self.submit_to_worker(file_id)

        current_status = {
            'job_id': job_id,
            'status': 'queued'
        }

        # send status of job to monitor
        self.__monitor.send_json(current_status)

        # Job created
        return current_status, 202

    def prepare_result(self, data):
        return FileUtil.create_result(uuid.uuid1().int, data)

    def parse_args(self):
        self.parser.add_argument(
            'elements',
            type=dict,
            required=True,
            help='Elements'
        )
        self.parser.add_argument(
            'data',
            type=dict,
            required=True,
            help='Network Attr'
        )

    def submit_to_worker(self, input_data_location):
        # Generate unique job ID
        job_id = str(uuid.uuid4())

        # The worker will get location of data, not actual data.
        task = {
            'job_id': job_id,
            'data': INPUT_DATA_SERVER_LOCATION + 'data/' + input_data_location
        }

        logging.debug('Task JSON = ' + str(task))
        self.__sender.send_json(task)

        return job_id
