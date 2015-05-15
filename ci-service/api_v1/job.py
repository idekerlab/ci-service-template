# -*- coding: utf-8 -*-
import os
import logging

from flask.ext.restful import Resource
from rq.job import Job, JobStatus
import rq.exceptions

from jobs import redis_conn, q, job_list
from . import RESULT_TYPE, RESULT_FILE
from utils.file_util import FileUtil


class SingleJob(Resource):

    def get(self, job_id):

        try:
            job = Job.fetch(job_id, connection=redis_conn)
        except rq.exceptions.NoSuchJobError:
            not_found = {
                'message': 'Job ' + job_id + ' does not exist.'
            }
            return not_found, 404

        # Return status of the job
        status = {
            'job_id': job_id,
            'status': job.get_status(),
            'result_url': 'jobs/' + job.get_id() + '/result',
            'result_type': job.meta['result_type']
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
            filename = FileUtil.get_result_file_location(file_id)
            logging.debug('Deleting: ' + str(filename))
            os.remove(filename)

        job_list.remove(job.get_id())
        q.remove(job)

        result = {
            'message': 'Job ' + job_id + ' removed.'
        }

        return result, 200
