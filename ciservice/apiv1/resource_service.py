import uuid
import logging

from flask.ext.restful import Resource
import zmq
import redis
from flask import request
import requests as client
from util_service import ServiceUtil

STATUS_PORT = 6666
INPUT_DATA_SERVER_LOCATION = 'http://dataserver:3000/'

logging.basicConfig(level=logging.DEBUG)


class ServiceResource(Resource):
    """
    Sample API for calling new worker pool
    """

    def __init__(self):
        super(ServiceResource, self).__init__()
        self.__context = zmq.Context()

        self.__monitor = self.__context.socket(zmq.PUSH)
        self.__monitor.connect('tcp://collector:' + str(STATUS_PORT))

        self.__sockets = {}
        self.__redis_conn = redis.Redis('redis', 6379)
        self.__util = ServiceUtil()

    def get(self, name):
        """
        Details of this service

        :return: Details about this service.
        """
        return self.__util.get_service_details(name), 200

    def post(self, name):
        """
        POST a new job to a service

        :return:
        """
        logging.debug('Service name: ' + name)

        # Stream the input data to file server (data cache server).
        req = client.post(INPUT_DATA_SERVER_LOCATION + 'data',
                          json=request.stream.read(),
                          stream=True)

        logging.debug('File server response Data = ' + str(req.json()))

        # This is a unique file ID for this input data
        file_id = req.json()['fileId']

        # ID of this new job
        job_id = self.submit_to_worker(file_id, name)

        # Save the key-value pair (Job ID to input file ID)
        #    - This will be used for deletion.
        input_file_location = INPUT_DATA_SERVER_LOCATION + 'data/' + file_id
        self.__redis_conn.hset(name='input-file', key=job_id, value=input_file_location)

        current_status = {
            'job_id': job_id,
            'status': 'queued'
        }

        logging.debug('Sending status: ' + str(current_status))

        # send status of job to monitor
        self.__monitor.send_json(current_status)

        # Job created
        return current_status, 202

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

        logging.debug('Endpoints = ' + str(registered))

        if service_name not in registered.keys():
            raise ValueError('No such service: ' + service_name)

        send_port = registered[service_name]

        logging.debug('target Port = ' + str(send_port))

        if service_name not in self.__sockets.keys():
            send_socket = self.__context.socket(zmq.PUSH)
            send_socket.bind('tcp://*:' + str(send_port))
            self.__sockets[service_name] = send_socket
        else:
            send_socket = self.__sockets[service_name]

        logging.debug('Sending data....')

        send_socket.send_json(task)

        return job_id
