# -*- coding: utf-8 -*-

import yaml


class ConfigParser(object):

    @staticmethod
    def parse(config_file_name):
        config_file = open(config_file_name)
        config = config_file.read()
        data = yaml.load(config)

        config_file.close()

        return data
