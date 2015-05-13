from networkx import nx
from py2cytoscape import util
from base_service import MemoryResultService
from utils.logger_factory import LoggerUtil

logger = LoggerUtil.get_logger(__name__)


class StatisticsService(MemoryResultService):

    def parse_args(self):
        self.parser.add_argument('elements', type=dict, required=True, help='Elements')
        self.parser.add_argument('data', type=dict, required=True, help='Network Attr')


class Betweenness(StatisticsService):
    def run_service(self, data):
        logger.debug('Calculating betweenness.')
        nx_graph = util.to_networkx(data)
        return nx.betweenness_centrality(nx_graph)


class PageRank(StatisticsService):
    def run_service(self, data):
        logger.debug('Calculating PageRank.')
        nx_graph = util.to_networkx(data)
        return nx.pagerank_scipy(nx_graph)


class Clustering(StatisticsService):
    def run_service(self, data):
        logger.debug('Calculating clustering coefficients.')
        nx_graph = util.to_networkx(data)
        return nx.clustering(nx_graph)
