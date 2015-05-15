# -*- coding: utf-8 -*-

from flask.ext.restful import Resource
from rq.job import Job
import rq.exceptions
from flask import Response

from jobs import redis_conn
from . import RESULT_TYPE, RESULT_FILE
from utils.file_util import FileUtil


class Result(Resource):

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
