import unittest

import networkx as nx
from py2cytoscape import util


class TestGraphAnalysisAlgorithms(unittest.TestCase):
    def setUp(self):
        # Generate a sample graph
        self.graph = util.from_networkx(nx.barabasi_albert_graph(100, 2))

    def test_betweenness(self):
        from ..apiv1.services.graph_analysis_algorithms import Betweenness

        bwn = Betweenness()
        result = bwn.calculate(self.graph)

        self.assertIsNotNone(result)
        self.assertEqual(dict, type(result))
        self.assertEqual(100, len(result))
