# -*- coding: utf-8 -*-

from flask.ext.restful import Resource
from flask import redirect, url_for

import zmq
import redis
import logging
import requests

from flask import Response
from flask import stream_with_context, redirect

logging.basicConfig(level=logging.DEBUG)


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

    def __init__(self, fetch=FETCH_PORT, status=STATUS_PORT, redisp=6379):
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

        self.__redis_connection = redis.Redis(host='redis', port=redisp, db=0)

    def get(self, job_id):
        """
        GET result.
        :return: response
        """
        result_location = self.__redis_connection.hget(name='results', key=job_id)
        logging.debug('!!!!!!!!!! 4 Fetching result: ' + str(result_location))

        # Stream the result from the file server
        import time
        start = time.clock()
        req = requests.get(str(result_location), stream=True)
        end = time.clock()
        logging.debug('TIME: ' + str(end-start))

        return Response(req.content, mimetype='application/json')


    def delete(self):
        return 200
