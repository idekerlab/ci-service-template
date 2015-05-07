from flask.ext import restful

from networkx import nx
from py2cytoscape import util
from flask.ext.restful import reqparse
from jobs import q, job_list

from . import logger, API_VERSION
import requests

from .utils.file_writer import FileUtil

import uuid
import os
import json

import tags

# Lifetime of the results
RESULT_TIME_TO_LIVE = 500000

# Timeout for this task is 1 week
TIMEOUT = 60*60*24*7


class GraphGeneratorService(restful.Resource):
    """
    Sample service to use temp file for storing result.
    """

    def __init__(self):
        # self.APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
        self.file_util = FileUtil()
        self.__parser = reqparse.RequestParser()

    def post(self):
        """
        Create and submit a new graph analysis job in the queue.
        :return:
        """
        self.__parser.add_argument('num_nodes', type=int, help='Number of Nodes')
        graph_info = self.__parser.parse_args()

        # Send the time-consuming job to workers
        job = q.enqueue_call(
            func=self.generate,
            args=(graph_info,),
            timeout=RESULT_TIME_TO_LIVE, result_ttl=RESULT_TIME_TO_LIVE)
        job_list.append(job.get_id())

        # Set optional parameter.  Result will be saved to file
        job.meta['result_type'] = 'file'
        job.save()

        job_info = {
            'job_id': job.get_id(),
            'status': job.get_status(),
            'url': API_VERSION + 'jobs/' + job.get_id(),
            'result_type': job.meta['result_type']
        }

        # Job created.
        return job_info, 202

    def generate(self, params):
        pass


class ScaleFree(GraphGeneratorService):
    """
    Random graph generator using NetworkX's Scale-Free graph generator.
    """

    def generate(self, params):
        graph = nx.scale_free_graph(params['num_nodes'])
        cyjs = util.from_networkx(graph)
        return self.file_util.create_result(uuid.uuid1().int, cyjs)