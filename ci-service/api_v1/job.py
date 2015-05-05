# -*- coding: utf-8 -*-

"""
API to access a specific job.
"""

from flask.ext import restful
from rq.job import Job
from jobs import redis_conn, q, job_list
import rq.exceptions
from rq.job import JobStatus

from tags import *
import os


from flask import Response

class SingleJob(restful.Resource):

    def __init__(self):
        self.APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top

    def __stream_file(self, file_id):

        def generate(result_file_name):
            filename = os.path.join(self.APP_ROOT, 'results/' + result_file_name)
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
                result_file = job.result['file']
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

        q.remove(job)
        job_list.remove(job)

        return {'message': 'Job ' + job_id + ' removed.'}, 200