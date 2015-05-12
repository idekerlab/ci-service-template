# -*- coding: utf-8 -*-

"""
API to access a specific job.
"""

import os

from flask.ext import restful
from rq.job import Job
import rq.exceptions
from rq.job import JobStatus
from flask import Response

from jobs import redis_conn, q, job_list
from . import logger
from utils.file_util import FileUtil

RESULT_TYPE = 'result_type'
RESULT_FILE = 'file'


class SingleJob(restful.Resource):

    def __stream_file(self, file_id):

        def generate(result_file_name):
            filename = FileUtil.get_result_file_location(result_file_name)

            f = open(filename)
            for line in f:
                yield line

        return Response(generate(file_id))

    def get(self, job_id):

        try:
            job = Job.fetch(job_id, connection=redis_conn)
        except rq.exceptions.NoSuchJobError:
            not_found = {
                'message': 'Job ' + job_id + ' does not exist.'
            }
            return not_found, 404

        if job.is_finished:
            result_type = job.meta[RESULT_TYPE]
            if result_type == RESULT_FILE:
                # Result contains file location (as UUID)
                result_file = job.result[RESULT_FILE]
                return self.__stream_file(result_file)
            else:
                # Simply return result directly from
                return job.result, 200
        else:
            # Return status if not available.
            status = {
                'job_id': job_id,
                'status': job.get_status()
            }
            return status, 200

    def delete(self, job_id):
        """
        Delete a job from queue.

        :return:
        """

        # Check task exists or not.
        try:
            job = Job.fetch(job_id, connection=redis_conn)
        except rq.exceptions.NoSuchJobError:
            not_found = {
                'message': 'Job ' + job_id + ' does not exist.'
            }
            return not_found, 404

        status = job.get_status()
        if status is JobStatus.STARTED:
            job.cancel()

        # Extra cleanup required: Remove temp file if necessary
        result_type = job.meta[RESULT_TYPE]
        if result_type == RESULT_FILE:
            file_id = job.result['file']
            filename = self.file_util.get_result_file_location(file_id)
            logger.debug('deleting: ' + str(filename))
            os.remove(filename)

        job_list.remove(job.get_id())
        q.remove(job)

        result = {
            'message': 'Job ' + job_id + ' removed.'
        }

        return result, 200
