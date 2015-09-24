# -*- coding: utf-8 -*-

import logging

from flask.ext.restful import Resource
import redis

from . import TAG_JOB_ID, TAG_STATUS

logging.basicConfig(level=logging.DEBUG)


class Task(Resource):
    """
    Show task status
    """

    def __init__(self, redisp=6379):
        super(Task, self).__init__()
        self.__redis_connection = redis.Redis(host='redis', port=redisp, db=0)

    def get(self, job_id):
        """
        GET status of the task.
        :return: response
        """
        status = self.__redis_connection.hget(name='status', key=job_id)
        logging.debug('Got status: ' + str(status))
        result = {
            TAG_JOB_ID: job_id,
            TAG_STATUS: status
        }
        return result, 200
