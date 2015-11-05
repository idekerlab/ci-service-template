# -*- coding: utf-8 -*-
import unittest
import os

from ciworker.config_parser import ConfigParser


class TestConfigParser(unittest.TestCase):

    def test_parse_config(self):

        print('\n\n----------  Config Parser Test Start -------------\n')

        config_file = 'config.yml'
        full_path = os.path.join(os.path.dirname(__file__), config_file)

        config_data = ConfigParser.parse(full_path)

        self.assertIsNotNone(config_data)

        print(repr(config_data))

        self.assertEqual(1, len(config_data))
        hello = config_data['hello']

        self.assertIsNotNone(hello)

        endpoint = hello['endpoint']

        self.assertEqual('hello-python', endpoint)


        print('\n----------  Config Parser Test Finished -------------\n')
