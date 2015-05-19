# -*- coding: utf-8 -*-
import logging

from flask.ext.restful import Resource

from resource_base import MemoryResultResource, RESULT_MEMORY
from services.graph_analysis_algorithms import GraphAnalysisAlgorithms, \
    Betweenness, PageRank

# Actual instance of services
algorithms = GraphAnalysisAlgorithms()
algorithms.register(Betweenness())
algorithms.register(PageRank())


class GraphAlgorithmResource(Resource):
    """
    List of all available algorithms
    """

    def get(self):
        return algorithms.get_all_algorithm_names()


class MemoryResultExampleResource(MemoryResultResource):
    def post(self, algorithm_name):
        """
        Create and submit a new graph analysis job in the queue.
        :return:
        """
        self.parse_args()
        data = self.parser.parse_args()
        data['algorithm_name'] = algorithm_name
        return self.submit(self.run_service, data,
                           result_type=RESULT_MEMORY), 202

    def parse_args(self):
        self.parser.add_argument(
            'elements',
            type=dict,
            required=True,
            help='Elements'
        )
        self.parser.add_argument(
            'data',
            type=dict,
            required=True,
            help='Network Attr'
        )

    def run_service(self, data):
        """
        Directly return statistics as list

        :param data: Must contain algorithm name, and Cytoscape.js style
        graph object

        :return: List of statistics
        """
        algorithm_name = data['algorithm_name']
        algorithm = algorithms.get_algorithm(algorithm_name)

        logging.getLogger(__name__).debug('Calculating ' + algorithm_name)

        return algorithm.calculate(data)
