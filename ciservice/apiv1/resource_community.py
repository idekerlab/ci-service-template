import uuid
import zmq
import logging

from .resource_base import BaseResource
from .utils.file_util import FileUtil

ROUTER_PORT = 5557


class CommunityDetectionResource(BaseResource):

    def __init__(self):
        super().__init__()
        # Message bass
        context = zmq.Context()
        # Socket to send messages on
        self.__sender = context.socket(zmq.PUSH)
        self.__sender.bind('tcp://*:' + str(ROUTER_PORT))


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

    def submit_to_router(self, data):
        # Generate a job ID
        job_id = str(uuid.uuid1())

        task = {
            'job_id': job_id,
            'data': data
        }
        self.__sender.send_json(task)

        return job_id
