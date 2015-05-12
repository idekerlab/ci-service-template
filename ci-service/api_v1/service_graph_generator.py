import uuid

import base_service
from networkx import nx
from py2cytoscape import util

from . import task_logger

from .utils.file_util import FileUtil

# Logger for queued tasks
# task_logger = LoggerUtil.get_logger(__name__)


class GraphGeneratorService(base_service.BaseService):
    """
    Random graph generator using NetworkX's Scale-Free graph generator.
    """

    def parse_args(self):
        self.parser.add_argument('num_nodes', type=int, help='Number of Nodes')

    def run_service(self, data):
        task_logger.debug('Generate job started')

        graph = nx.scale_free_graph(data['num_nodes'])
        result = util.from_networkx(graph)

        task_logger.debug('Generate job finished')

        return FileUtil.create_result(uuid.uuid1().int, result)
