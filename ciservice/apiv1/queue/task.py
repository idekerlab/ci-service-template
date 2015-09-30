# -*- coding: utf-8 -*-
import logging

from flask.ext.restful import Resource
import redis
import requests

from . import TAG_JOB_ID, TAG_STATUS
from apiv1.queue.util_task import TaskUtil

INPUT_DATA_SERVER_LOCATION = 'http://dataserver:3000/'

logging.basicConfig(level=logging.DEBUG)


class Task(Resource):
    """
    Show task status
    """

    def __init__(self, redisp=6379):
        super(Task, self).__init__()
        self.__redis_connection = redis.Redis(host='redis', port=redisp, db=0)
        self.__util = TaskUtil()

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

    def delete(self, job_id):
        """Delete both job and its result.
        :return: Success message
        """
        return self.__util.delete_job(job_id), 200
