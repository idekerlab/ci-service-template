from flask.ext import restful

from flask.ext.restful import reqparse
from jobs import q, job_list
from flask import Response
import os


# Lifetime of the results.
RESULT_TIME_TO_LIVE = 500000


class StreamingService(restful.Resource):

    def __init__(self):
        self.APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
        self.__parser = reqparse.RequestParser()

    def get(self, job_id):

        def generate(result_file_name):
            filename = os.path.join(self.APP_ROOT, 'results/' + result_file_name)
            f = open(filename)
            for line in f:
                yield line

        return Response(generate(job_id))
