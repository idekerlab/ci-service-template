# -*- coding: utf-8 -*-

from flask.ext.restful import Resource


import zmq


QUEUED = 'queued'
FINISHED = 'finished'
FAILED = 'failed'
STARTED = 'started'


class TaskQueue(Resource):
    """
    API for job management.
    """

    def __init__(self):
        super(TaskQueue, self).__init__()
        # Data producer to send tasks to workers.
        context = zmq.Context()
        self.__socket = context.socket(zmq.REQ)
        self.__socket.connect('tcp://collector:5555')

    def get(self):
        """
        GET list of all jobs in the queue.
        :return: response
        """

        # Fetch job list from

        self.__socket.send_json({'command': 'GET_ALL'})
        message = self.__socket.recv_json()

        res = {'OK': message}
        return res, 200
