# -*- coding: utf-8 -*-
import argparse
import logging

from base_worker import BaseWorker


class KernelGeneratorWorker(BaseWorker):

    def run(self, data):

        result = {
            'message': 'Dummy result from kernel'
        }

        logging.debug('Calculated by ' + str(self.id))

        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start workers.')

    parser.add_argument('endpoint', type=str, help='Endpoint name.')
    parser.add_argument('id', type=int, help='worker ID.')
    parser.add_argument('router', type=str, help='router IP address.')
    parser.add_argument('collector', type=str, help='collector IP address.')
    parser.add_argument('port', type=int, help='port number of the router.')

    args = parser.parse_args()
    print('Listening to ' + args.router + ':' + str(args.port) + '...')

    worker = KernelGeneratorWorker(endpoint=args.endpoint, id=args.id, router=args.router,
                                   collector=args.collector,
                        receiver=args.port)
    worker.listen()
