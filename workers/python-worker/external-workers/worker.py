import sys
import time
import zmq
import uuid
import logging
import argparse

import networkx as nx

REC_PORT = 5557
SEND_PORT = 5558


class Worker(object):
    """
    Minimalistic python-worker implementation for python
    """
    def __init__(self, id, router, collector, receiver=REC_PORT, sender=SEND_PORT):
        self.__id = 'External: ' + str(id)
        logging.basicConfig(level=logging.DEBUG)

        self.__router = router
        

        # 0MQ context
        context = zmq.Context()

        # For accepting input
        self.__receiver = context.socket(zmq.PULL)
        self.__receiver.connect('tcp://' + router + ':' + str(receiver))

        # For sending out the result
        self.__sender = context.socket(zmq.PUSH)
        self.__sender.connect('tcp://' + collector + ':' + str(sender))


    def __create_status(self, job_id):
        status = {
            'job_id': job_id,
            'worker_id': str(self.__id),
            'status': 'running'
        }
        return status


    def listen(self):
        # Start listening...
        logging.info('Worker start: ID = ' + str(self.__id))
        logging.info('IP = ' + str(self.__router))

        while True:
            data = self.__receiver.recv_json()

            # Validate data
            # TODO: Exception handler
            if 'job_id' in data.keys():
                jid = data['job_id']
            else:
                raise ValueError('job_id is missing.')

            # Tell collector the job is running.
            self.__sender.send_json(self.__create_status(jid))

            # Extract JSON

            # Do some real work....
            result = self.__run(data='')

            result = {
                'worker_id': str(self.__id),
                'job_id': jid,
                'result': result
            }

            # Send results to sink
            self.__sender.send_json(result)

    def __run(self, data):
        g = nx.scale_free_graph(1000)
        bet = nx.betweenness_centrality(g)
        logging.info('@Calculated by external:  ' + str(self.__id))
        return bet


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start python-worker.')

    parser.add_argument('id', type=int, help='worker ID.')
    parser.add_argument('router', type=str, help='router IP address.')
    parser.add_argument('collector', type=str, help='collector IP address.')
    parser.add_argument('port', type=int, help='port number of the router.')

    args = parser.parse_args()
    print('Listening to ' + args.router + ':' + str(args.port) + '...')

    worker = Worker(id=args.id, router=args.router, collector=args.collector, receiver=args.port)
    worker.listen()
