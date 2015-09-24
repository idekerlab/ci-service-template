import uuid
import zmq
import logging
import redis

from flask import request
import requests as client

from .resource_base import BaseResource
from .utils.file_util import FileUtil

STATUS_PORT = 6666

INPUT_DATA_SERVER_LOCATION = 'http://dataserver:3000/'

logging.basicConfig(level=logging.DEBUG)


class SubmitResource(BaseResource):
    """
    Sample API for calling new worker pool
    """

    def __init__(self):
        super(SubmitResource, self).__init__()
        # Data producer to send tasks to workers.
        self.__context = zmq.Context()

        self.__monitor = self.__context.socket(zmq.PUSH)
        self.__monitor.connect('tcp://collector:' + str(STATUS_PORT))

        self.__sockets = {}
        self.__redis_conn = redis.Redis('redis', 6379)

    def get(self):
        """
        Simply return description of this service

        :return:
        """
        description = {
            'message': 'Use POST method to submit your graph data.'
        }

        return description, 200

    def post(self, name):
        """
        POST network data to queue

        :return:
        """
        logging.debug('Task name: ' + name)

        req = client.post(INPUT_DATA_SERVER_LOCATION + 'data', json=request.stream.read(),
                          stream=True)
        logging.debug('File server response Data = ' + str(req.json()))
        file_id = req.json()['fileId']

        job_id = self.submit_to_worker(file_id, name)

        current_status = {
            'job_id': job_id,
            'status': 'queued'
        }

        logging.debug('Sending status: ' + str(current_status))

        # send status of job to monitor
        self.__monitor.send_json(current_status)

        # Job created
        return current_status, 202

    def prepare_result(self, data):
        return FileUtil.create_result(uuid.uuid1().int, data)

    def submit_to_worker(self, input_data_location, service_name):
        # Generate unique job ID
        job_id = str(uuid.uuid4())

        # The worker will get location of data, not actual data.
        task = {
            'job_id': job_id,
            'data': INPUT_DATA_SERVER_LOCATION + 'data/' + input_data_location
        }

        logging.debug('Task JSON = ' + str(task))
        registered = self.__redis_conn.hgetall('endpoints')
        if service_name not in registered.keys():
            raise ValueError('No such service: ' + service_name)

        send_port = registered[service_name]
        if service_name not in self.__sockets.keys():
            send_socket = self.__context.socket(zmq.PUSH)
            send_socket.bind('tcp://*:' + str(send_port))
            self.__sockets[service_name] = send_socket
        else:
            send_socket = self.__sockets[service_name]

        send_socket.send_json(task)

        return job_id
