import unittest


class TestGraphAnalysisService(unittest.TestCase):

    def setUp(self):
        pass

    def test_run_service(self):
        from api_v1.tasks.graph_factory import GraphFactory

        num_nodes = 100
        result = GraphFactory.get_scale_free_graph(num_nodes)

        print(result)
