# -*- coding: utf-8 -*-

"""API for all jobs in this system

"""

from flask.ext import restful
from rq import Queue
from rq.job import Job
from rq.job import JobStatus
from redis import Redis

redis_conn = Redis('redis', 6379)
q = Queue(connection=redis_conn)

# List of jobs
job_list = []


class Jobs(restful.Resource):

    """
    API for job management.
    """
    def get(self):
        """
        GET list of all jobs in the system.
        :return: response
        """
        res = []
        for job_id in job_list:
            job = Job.fetch(job_id, connection=redis_conn)
            job_obj = {
                'job_id': job_id,
                'status': job.get_status()
            }
            res.append(job_obj)

        return res, 200

    def delete(self):
        """
        Delete all jobs from system.

        :return:
        """

        for job_id in job_list:
            job = Job.fetch(job_id, connection=redis_conn)
            status = job.get_status()
            if status is JobStatus.STARTED:
                job.cancel()

        q.empty()
        del job_list[:]

        return {'message': 'All jobs removed.'}, 200