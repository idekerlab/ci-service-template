# -*- coding: utf-8 -*-
import logging

from flask.ext.restful import Resource
import redis
import requests

from . import TAG_JOB_ID, TAG_STATUS

INPUT_DATA_SERVER_LOCATION = 'http://dataserver:3000/'

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

    def delete(self, job_id):
        """
        Delete both job and its result.
        :return: Success message
        """
        logging.debug('Got deletion request for: ' + str(job_id))

        # Delete both input and result cache files
        result_location = self.__redis_connection.hget(name='results', key=job_id)
        logging.debug('Deleting result file: ' + str(result_location))

        input_cache_location = self.__redis_connection.hget(name='input-file',
                                                      key=job_id)
        # Result file
        req = requests.delete(result_location)
        logging.debug(str(req.json()))

        # Input file
        req = requests.delete(input_cache_location)
        logging.debug(str(req.json()))

        # Delete from status list
        self.__redis_connection.hdel(TAG_STATUS, (job_id))

        # TODO: send status of job to monitor
        # self.__monitor.send_json(current_status)

        result = {
            TAG_JOB_ID: job_id,
            TAG_STATUS: 'deleted'
        }
        return result, 200
