# -*- coding: utf-8 -*-

from .config_parser import ConfigParser


class WorkerBuilder():

    @staticmethod
    def create_worker(config_file_name):

        config_data = ConfigParser.parse(config_file_name)



