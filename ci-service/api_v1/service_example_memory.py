import logging

from flask.ext.restful import Resource
from base_service import MemoryResultService, RESULT_MEMORY

from tasks.graph_analysis_algorithms import GraphAnalysisAlgorithms, Betweenness, PageRank, Clustering

algorithms = GraphAnalysisAlgorithms()
algorithms.register(Betweenness())
algorithms.register(PageRank())
algorithms.register(Clustering())


class GraphAnalysis(Resource):

    def get(self):
        return algorithms.get_all_algorithm_names()


class MemoryResultServiceExample(MemoryResultService):

    def post(self, algorithm_name):
        """
        Create and submit a new graph analysis job in the queue.
        :return:
        """
        self.parse_args()
        data = self.parser.parse_args()
        data['algorithm_name'] = algorithm_name
        return self.submit(self.run_service, data, result_type=RESULT_MEMORY), 202

    def parse_args(self):
        self.parser.add_argument('elements', type=dict, required=True, help='Elements')
        self.parser.add_argument('data', type=dict, required=True, help='Network Attr')

    def run_service(self, data):
        algorithm_name = data['algorithm_name']
        algorithm = algorithms.get_algorithm(algorithm_name)

        logging.getLogger(__name__).debug('Calculating ' + algorithm_name)

        return self.prepare_result(algorithm.calculate(data))
