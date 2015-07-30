# -*- coding: utf-8 -*-

from flask.ext.restful import Resource
from flask import redirect, url_for

import zmq


QUEUED = 'queued'
FINISHED = 'finished'
FAILED = 'failed'
STARTED = 'started'

# Port for fetching task status
FETCH_PORT = 5555

# Port for status monitor
STATUS_PORT = 7777

# Message template
COMMAND = {
    'command': None
}

class Task(Resource):
    """
    API for job management.
    """

    def __init__(self, fetch=FETCH_PORT, status=STATUS_PORT):
        super(Task, self).__init__()
        # Data producer to send tasks to workers.
        context = zmq.Context()

        ##### Connections to other modules #####

        # For fetching data from collector
        self.__result = context.socket(zmq.REQ)
        self.__result.connect('tcp://collector:' + str(fetch))

        # For status checking
        self.__status = context.socket(zmq.REQ)
        self.__status.connect('tcp://collector:' + str(status))

    def get(self, job_id):
        """
        GET result.
        :return: response
        """
        return redirect(url_for('http://collector:5001/results/' + str(job_id)))


    def delete(self):
        return 200
