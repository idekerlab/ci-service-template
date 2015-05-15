# -*- coding: utf-8 -*-

from flask.ext.restful import Resource
from rq.job import Job
import rq.exceptions
from flask import Response

from jobs import redis_conn
from . import RESULT_TYPE, RESULT_FILE
from utils.file_util import FileUtil
from utils.job_util import JobUtil


class Result(Resource):
    """Represents a result of a job
    If the job is finished, it returns result.  Otherwise, return status of it.
    """

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
            return JobUtil.get_not_found_message(job_id)

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
            return JobUtil.get_job_info(job)
