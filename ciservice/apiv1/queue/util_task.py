# -*- coding: utf-8 -*-
import redis
import logging
import requests
from . import TAG_JOB_ID, TAG_STATUS

logging.basicConfig(level=logging.DEBUG)


class TaskUtil():

    def __init__(self):
        self.__redis_connection = redis.Redis('redis', 6379)

    def delete_job(self, job_id):
        """Delete both job and its result.
        :return: Success message
        """
        logging.debug('Got deletion request for: ' + str(job_id))

        # Delete both input and result cache files
        result_location = self.__redis_connection.hget(name='results', key=job_id)
        logging.debug('Deleting result file: ' + str(result_location))

        input_cache_location = self.__redis_connection.hget(name='input-file',
                                                            key=job_id)
        # Result file
        if result_location is not None:
            req = requests.delete(result_location)
            #logging.debug(str(req.json()))

        # Input file
        if input_cache_location is not None:
            req = requests.delete(input_cache_location)
            #logging.debug(str(req.json()))

        # Delete from status list
        self.__redis_connection.hdel(TAG_STATUS, (job_id))

        # TODO: send status of job to monitor
        # self.__monitor.send_json(current_status)

        result = {
            TAG_JOB_ID: job_id,
            TAG_STATUS: 'deleted'
        }
        return result
