# -*- coding: utf-8 -*-

"""
API to access a specific job.
"""

from flask.ext import restful
from rq.job import Job
from jobs import redis_conn, q, job_list
import rq.exceptions
from rq.job import JobStatus


class SingleJob(restful.Resource):

    def get(self, job_id):
        try:
            job = Job.fetch(job_id, connection=redis_conn)
        except rq.exceptions.NoSuchJobError:
            not_found = {
                'message': 'Job ' + job_id + ' does not exist.'
            }
            return not_found, 404

        if job.is_finished:
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