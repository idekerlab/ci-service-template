import zmq
import logging
import argparse
import requests
import json
import redis

import requests as client

import networkx as nx
from py2cytoscape.util import *

REC_PORT = 5556
SEND_PORT = 5558

MONITOR_PORT = 6666

RESULT_SERVER_LOCATION = 'http://resultserver:3000/'

# TODO: add more samples

logging.basicConfig(level=logging.DEBUG)

class BaseWorker(object):
    """
    Minimalistic workers implementation for python
    """
    def __init__(self, id, router, collector,
                 receiver=REC_PORT, sender=SEND_PORT, monitor=MONITOR_PORT):

        self.__redis_conn = redis.Redis('redis', 6379)

        self.__id = id
        self.__router = router
        
        # 0MQ context
        context = zmq.Context()
        endpoint = 'community'

        registered = self.__redis_conn.hgetall('endpoints')
        if endpoint not in registered.keys():
            self.__redis_conn.hset('endpoints', endpoint, receiver)
            logging.info('Service registered: ' + endpoint + ', Port ' + str(receiver))

        # reg.send_json(endpoint)


        # For getting input data for this worker
        self.__receiver = context.socket(zmq.PULL)
        self.__receiver.connect('tcp://' + router + ':' + str(receiver))

        # For sending out the result to collector
        self.__sender = context.socket(zmq.PUSH)
        self.__sender.connect('tcp://' + collector + ':' + str(sender))

        # for status monitoring
        self.__monitor = context.socket(zmq.PUSH)
        self.__monitor.connect('tcp://collector:' + str(monitor))

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
            if 'job_id' in data.keys() and 'data' in data.keys():
                jid = data['job_id']
            else:
                raise ValueError('job_id or data location is missing.')

            # Tell collector the job is running.
            # self.__sender.send_json(self.__create_status(jid))

            self.__monitor.send_json(self.__create_status(jid))
            # Extract JSON

            # Do some real work....

            # Fetch data from file server
            data_location = data['data']
            logging.info('####### Data location => ' + str(data_location))

            response = requests.get(data_location)

            input_data = response.json()
            input_dict = json.loads(input_data)
            logging.info('***TYPE')
            logging.info(type(input_dict))

            final_result = self.__run(data=input_dict)

            req = client.post(RESULT_SERVER_LOCATION + 'data', json=final_result, stream=True)
            file_id = req.json()['fileId']

            logging.debug('Result File server response Data = ' + str(req.json()))

            result = {
                'worker_id': str(self.__id),
                'job_id': jid,
                'result': RESULT_SERVER_LOCATION + 'data/' + str(file_id)
            }

            # Send results to sink
            self.__sender.send_json(result)

    def __run(self, data):
        # This is thr section you can add any worker process...
        g = to_networkx(data)
        logging.debug('Data in: ' + str(g))

        result_json = nx.betweenness_centrality(g)

        logging.debug('Calculated by ' + str(self.__id))

        return result_json


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start workers.')

    parser.add_argument('id', type=int, help='worker ID.')
    parser.add_argument('router', type=str, help='router IP address.')
    parser.add_argument('collector', type=str, help='collector IP address.')
    parser.add_argument('port', type=int, help='port number of the router.')

    args = parser.parse_args()
    print('Listening to ' + args.router + ':' + str(args.port) + '...')

    worker = BaseWorker(id=args.id, router=args.router, collector=args.collector,
                       receiver=args.port)
    worker.listen()
