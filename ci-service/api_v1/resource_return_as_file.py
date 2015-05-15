# -*- coding: utf-8 -*-
from services.graph_factory import GraphFactory
from resource_base import FileResultResource


class FileResultExampleResource(FileResultResource):
    """
    Random graph generator using NetworkX's Scale-Free graph generator.
    """

    def parse_args(self):
        self.parser.add_argument('num_nodes', type=int, help='Number of Nodes')

    def run_service(self, data):
        # Convert result into file and its location.
        return self.prepare_result(GraphFactory.get_scale_free_graph(data['num_nodes']))
