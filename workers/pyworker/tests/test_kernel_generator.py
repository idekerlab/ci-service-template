import unittest
import json


class KernelGeneratorTests(unittest.TestCase):

    def setUp(self):
        self.finder = SciPyKernel()

    def test_find_sub_network(self):
        print('\n---------- Sub Network Finder tests start -----------\n')

        print('\n---------- finder tests finished! -----------\n')
