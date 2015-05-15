import unittest


class TestGraphAnalysisService(unittest.TestCase):

    def setUp(self):
        pass

    def test_run_service(self):
        from api_v1.services.graph_factory import GraphFactory

        num_nodes = 100
        scale_free_graph_100 = GraphFactory.get_scale_free_graph(num_nodes)

        nodes = scale_free_graph_100['elements']['nodes']
        edges = scale_free_graph_100['elements']['edges']
        network_data = scale_free_graph_100['data']
        self.assertIsNotNone(nodes)
        self.assertIsNotNone(edges)
        self.assertIsNotNone(network_data)
        self.assertEqual(100, len(nodes))
        self.assertTrue(100 < len(edges))
