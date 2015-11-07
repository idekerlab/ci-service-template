# -*- coding: utf-8 -*-

import logging
from multiprocessing import Process

from ciworker import arg_parser as parser

from ciworker.config_parser import ConfigParser
from ciworker.id_generator import IdGenerator

logging.basicConfig(level=logging.DEBUG)


def start_worker(worker_factory, config_data, worker_id):
    hello_worker = worker_factory(config=config_data, id=worker_id)
    hello_worker.listen()


def get_factory(worker_name):
    parts = worker_name.split('.')
    logging.info('mod = ' + parts[0])
    logging.info('name = ' + parts[1])

    mod = __import__(parts[0])
    worker_factory = getattr(mod, parts[1])

    return worker_factory


if __name__ == '__main__':
    args = parser.get_args()
    config_file = args.config

    logging.info('Config file = ' + config_file)

    config = ConfigParser.parse(config_file)
    for key in config.keys():
        config_data = config[key]
        logging.info('Config Data = ' + str(config))
        num_workers = config_data['instances']
        worker_name = config_data['worker']
        id_generator = IdGenerator()

        worker_factory = get_factory(worker_name)

        for i in range(int(num_workers)):
            id = id_generator.next_id()
            p = Process(target=start_worker,
                        args=(worker_factory, config_data, id,))
            p.start()
