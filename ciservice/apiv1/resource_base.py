# -*- coding: utf-8 -*-
import uuid

from flask.ext.restful import Resource, reqparse

from queue.jobs import q, job_list
from utils.file_util import FileUtil
from . import RESULT_FILE, RESULT_MEMORY, RESULT_TYPE


# Lifetime of the results
RESULT_TIME_TO_LIVE = 500000

# Timeout for this task is 1 week
TIMEOUT = 60 * 60 * 24 * 7


class BaseResource(Resource):
    """
    Sample service to use temp file for storing result.
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()

    def get(self):
        message = {
            'message': 'Service called.  Use POST to submit your job.',
        }

        return message, 200

    def submit(self, function_name, data, result_type=RESULT_FILE,
               time_out=TIMEOUT, result_ttl=RESULT_TIME_TO_LIVE):
        job = q.enqueue_call(func=function_name, args=(data,),
                             timeout=time_out,
                             result_ttl=result_ttl)
        job_list.append(job.get_id())

        # set optional parameter.  result will be saved to file
        job.meta[RESULT_TYPE] = result_type
        job.save()

        job_info = {
            'job_id': job.get_id(),
            'status': job.get_status(),
            'url': 'queue/' + job.get_id(),
            'result_type': job.meta['result_type']
        }
        return job_info

    def parse_args(self):
        return None

    def run_service(self, data):
        pass

    def prepare_result(self, data):
        return data


class FileResultResource(BaseResource):
    def post(self):
        """
        Create and submit a new graph analysis job in the queue.
        :return:
        """
        self.parse_args()
        data = self.parser.parse_args()
        return self.submit(self.run_service, data,
                           result_type=RESULT_FILE), 202

    def prepare_result(self, data):
        return FileUtil.create_result(uuid.uuid1().int, data)


class MemoryResultResource(BaseResource):
    def post(self):
        """
        Create and submit a new graph analysis job in the queue.
        :return:
        """
        self.parse_args()
        data = self.parser.parse_args()
        return self.submit(self.run_service, data,
                           result_type=RESULT_MEMORY), 202
