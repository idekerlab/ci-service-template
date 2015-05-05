from flask.ext import restful

from networkx import nx
from py2cytoscape import util
from flask.ext.restful import reqparse
from jobs import q, job_list

import uuid
import os
import json

# Lifetime of the results.
RESULT_TIME_TO_LIVE = 500000

class GraphGeneratorService(restful.Resource):

    def __init__(self):
        self.APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
        self.__parser = reqparse.RequestParser()

    def post(self):
        """
        Create and submit a new graph analysis job in the queue.
        :return:
        """
        self.__parser.add_argument('num_nodes', type=int, help='Number of Nodes')
        graph_info = self.__parser.parse_args()

        # Send the time-consuming job to workers
        job = q.enqueue_call(func=self.generate, args=(graph_info,), result_ttl=RESULT_TIME_TO_LIVE)
        job_list.append(job.get_id())

        # Set optional parameter.  Result will be saved to file
        job.meta['result_type'] = 'file'
        job.save()

        job_info = {
            'job_id': job.get_id(),
            'status': job.get_status(),
            'url': '/v1/jobs/' + job.get_id(),
            'result_type': job.meta['result_type']
        }

        # Job created.
        return job_info, 202

    def generate(self, params):
        pass


class ScaleFree(GraphGeneratorService):

    def generate(self, params):
        file_id = uuid.uuid1()

        graph = nx.scale_free_graph(params['num_nodes'])
        cyjs = util.from_networkx(graph)

        filename = os.path.join(self.APP_ROOT, 'results/' + str(file_id.int))

        print(str(filename))
        tempfile = open(filename, 'w')
        json.dump(cyjs, tempfile)
        tempfile.close()

        result = {
            'file': str(file_id.int)
        }

        return result