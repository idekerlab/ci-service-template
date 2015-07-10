import uuid
import zmq
import redis
import logging

from .resource_base import BaseResource
from .utils.file_util import FileUtil

ROUTER_PORT = 5556

logging.basicConfig(level=logging.DEBUG)

class CommunityDetectionResource(BaseResource):

    def __init__(self):
        super(CommunityDetectionResource, self).__init__()
        # Data producer to send tasks to workers.
        context = zmq.Context()
        # Push tasks to workers
        self.__sender = context.socket(zmq.PUSH)
        self.__sender.bind('tcp://*:' + str(ROUTER_PORT))

        self.__monitor = context.socket(zmq.PUSH)
        self.__monitor.connect('tcp://collector:6666')


    def get(self):
        # Test to send message
        jobid = self.submit_to_worker({})
        result = {
            'job_id': jobid,
            'status': 'queued'
        }
        self.__monitor.send_json(result)

        return result, 202

    def post(self):
        """
        Redirect result back to
        :return:
        """
        self.parse_args()
        data = self.parser.parse_args()
        result = {}
        return result, 202

    def prepare_result(self, data):
        return FileUtil.create_result(uuid.uuid1().int, data)

    def submit_to_worker(self, data):
        # Generate a job ID
        job_id = str(uuid.uuid1())

        task = {
            'job_id': job_id,
            'data': data
        }

        self.__sender.send_json(task)

        return job_id
