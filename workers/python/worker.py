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
    Minimalistic workers implementation for python
    """
    def __init__(self, router, receiver=REC_PORT, sender=SEND_PORT):
        self.__id = uuid.uuid4()
        logging.basicConfig(level=logging.DEBUG)
        

        # 0MQ context
        context = zmq.Context()

        # For accepting input
        self.__receiver = context.socket(zmq.PULL)
        self.__receiver.connect('tcp://'+ router + ':' + str(receiver))

        # For sending out the result
        self.__sender = context.socket(zmq.PUSH)
        self.__sender.connect('tcp://' + router + ':' + str(sender))


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

        while True:
            data = self.__receiver.recv_json()
            logging.info('###Worker: ' + str(self.__id) + ' got job.')
            print('This is print: ' + str(self.__id))

            # Validate data
            # TODO: Exception handler
            if 'job_id' in data.keys():
                jid = data['job_id']
            else:
                raise ValueError('job_id is missing.')

            # Tell collector the job is running.
            self.__sender.send_json(self.__create_status(jid))

            # Extract JSON

            sys.stdout.flush()

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
        logging.info('Running task on: ' + str(self.__id))
        g = nx.scale_free_graph(300)
        bet = nx.betweenness_centrality(g)
        return bet


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start workers.')

    parser.add_argument('router', type=str, help='router IP address.')
    parser.add_argument('port', type=int, help='port number of the router.')

    args = parser.parse_args()
    print('Listening to ' + args.router + ':' + str(args.port) + '...')

    worker = Worker(router=args.router, receiver=args.port)
    worker.listen()