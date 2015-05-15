# -*- coding: utf-8 -*-
import os
import logging

from flask.ext.restful import Resource
from rq.job import Job, JobStatus
import rq.exceptions

from jobs import redis_conn, q, job_list
from . import RESULT_TYPE, RESULT_FILE
from utils.file_util import FileUtil
from utils.job_util import JobUtil


class SingleJob(Resource):
    """A Job resource
    All queued jobs are represented as this resource
    """

    def get(self, job_id):
        """
        Returns status of the job

        :param job_id: Job ID in the queue
        :return: Status of job as dict
        """

        try:
            job = Job.fetch(job_id, connection=redis_conn)
        except rq.exceptions.NoSuchJobError:
            return JobUtil.get_not_found_message(job_id)

        # Return status of the job
        return JobUtil.get_job_info(job), 200

    def delete(self, job_id):
        """
        Delete a job from the queue

        :return:
        """

        # Check task exists or not.
        try:
            job = Job.fetch(job_id, connection=redis_conn)
        except rq.exceptions.NoSuchJobError:
            return JobUtil.get_not_found_message(job_id)

        status = job.get_status()
        if status is JobStatus.STARTED:
            job.cancel()

        # Extra cleanup required: Remove temp file if necessary
        result_type = job.meta[RESULT_TYPE]
        if result_type == RESULT_FILE:
            file_id = job.result['file']
            filename = FileUtil.get_result_file_location(file_id)
            logging.debug('Deleting: ' + str(filename))
            os.remove(filename)

        job_list.remove(job.get_id())
        q.remove(job)

        result = {
            'message': 'Job ' + job_id + ' removed.'
        }

        return result, 200
