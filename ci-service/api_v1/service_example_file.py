import logging

from tasks.graph_factory import GraphFactory
from base_service import FileResultService


class FileResultServiceExample(FileResultService):
    """
    Random graph generator using NetworkX's Scale-Free graph generator.
    """

    def parse_args(self):
        """
        Parse required arguments manually

        :return:
        """
        self.parser.add_argument('num_nodes', type=int, help='Number of Nodes')

    def run_service(self, data):
        logging.debug('Generating graph...')
        result = GraphFactory.get_scale_free_graph(data['num_nodes'])
        logging.debug('Graph generated!')

        return self.prepare_result(result)
