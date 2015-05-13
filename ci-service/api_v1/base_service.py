from flask.ext import restful
from flask.ext.restful import reqparse
from jobs import q, job_list

from . import RESULT_FILE, RESULT_MEMORY, RESULT_TYPE

# Lifetime of the results
RESULT_TIME_TO_LIVE = 500000

# Timeout for this task is 1 week
TIMEOUT = 60*60*24*7


class BaseService(restful.Resource):
    """
    Sample service to use temp file for storing result.
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()

    def get(self):
        message = {
            'message': 'Service called'
        }

        return message, 200

    def submit(self, function_name, data, result_type=RESULT_FILE, time_out=TIMEOUT, result_ttl=RESULT_TIME_TO_LIVE):
        job = q.enqueue_call(
            func=function_name,
            args=(data,),
            timeout=time_out,
            result_ttl=result_ttl)
        job_list.append(job.get_id())

        # set optional parameter.  result will be saved to file
        job.meta[RESULT_TYPE] = result_type
        job.save()

        job_info = {
            'job_id': job.get_id(),
            'status': job.get_status(),
            'url': 'jobs/' + job.get_id(),
            'result_type': job.meta['result_type']
        }
        return job_info

    def parse_args(self):
        return None

    def run_service(self, data):
        pass


class FileResultService(BaseService):

    def post(self):
        """
        Create and submit a new graph analysis job in the queue.
        :return:
        """
        self.parse_args()
        data = self.parser.parse_args()
        return self.submit(self.run_service, data, result_type=RESULT_FILE), 202


class MemoryResultService(BaseService):

    def post(self):
        """
        Create and submit a new graph analysis job in the queue.
        :return:
        """
        self.parse_args()
        data = self.parser.parse_args()
        return self.submit(self.run_service, data, result_type=RESULT_MEMORY), 202
