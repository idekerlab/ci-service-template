import logging

import networkx as nx
from py2cytoscape import util


class GraphAnalysisAlgorithm():
    def __init__(self):
        self.name = self.__class__.__name__.lower()

    def calculate(self, graph):
        pass


class Betweenness(GraphAnalysisAlgorithm):
    def calculate(self, graph):
        return nx.betweenness_centrality(util.to_networkx(graph))


class PageRank(GraphAnalysisAlgorithm):
    def calculate(self, graph):
        return nx.pagerank_scipy(util.to_networkx(graph))


class GraphAnalysisAlgorithms():
    def __init__(self):
        self.__algorithms = {}
        logging.getLogger(__name__).debug(
            'Graph analysis algorithm manager initialized.')

    def get_algorithm(self, name):
        return self.__algorithms[name]

    def register(self, algorithm):
        self.__algorithms[algorithm.name] = algorithm

    def get_all_algorithm_names(self):
        return self.__algorithms.keys()
