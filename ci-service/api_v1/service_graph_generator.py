import uuid
from networkx import nx
from py2cytoscape import util
from base_service import FileResultService
from .utils.file_util import FileUtil
from utils.logger_factory import LoggerUtil

logger = LoggerUtil.get_logger(__name__)


class GraphGeneratorService(FileResultService):
    """
    Random graph generator using NetworkX's Scale-Free graph generator.
    """

    def parse_args(self):
        self.parser.add_argument('num_nodes', type=int, help='Number of Nodes')

    def run_service(self, data):
        logger.debug('Generate job started')

        graph = nx.scale_free_graph(data['num_nodes'])
        result = util.from_networkx(graph)

        logger.debug('Generate job finished')

        return FileUtil.create_result(uuid.uuid1().int, result)
