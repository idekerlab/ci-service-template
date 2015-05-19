import networkx as nx
from py2cytoscape import util


class GraphFactory():
    @staticmethod
    def get_scale_free_graph(num_nodes):
        """
        Generate scale-free graph with NetworkX

        :param num_nodes: Number of nodes in the generated network

        :return: Scale-free graph in Cytoscape.js format
        """
        graph = nx.scale_free_graph(num_nodes)
        return util.from_networkx(graph)
