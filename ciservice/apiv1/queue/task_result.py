# -*- coding: utf-8 -*-

from flask.ext.restful import Resource

import redis
import logging
import requests

from flask import Response

logging.basicConfig(level=logging.DEBUG)


class TaskResult(Resource):

    def __init__(self, redisp=6379):
        super(TaskResult, self).__init__()
        self.__redis_connection = redis.Redis(host='redis', port=redisp, db=0)

    def get(self, job_id):
        """
        GET result.
        :return: response
        """
        result_location = self.__redis_connection.hget(name='results', key=job_id)
        logging.debug('Fetching result from: ' + str(result_location))

        # Stream the result from the file server
        import time
        start = time.clock()
        req = requests.get(str(result_location), stream=True)
        end = time.clock()
        logging.debug('TIME: ' + str(end-start))

        return Response(req.content, mimetype='application/json')
