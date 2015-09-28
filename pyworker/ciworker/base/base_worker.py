import zmq
import logging
import json
import redis
import requests as client

SEND_PORT = 5558
MONITOR_PORT = 6666

RESULT_SERVER_LOCATION = 'http://resultserver:3000/'
REDIS_SERVER_LOCATION = 'redis'

logging.basicConfig(level=logging.DEBUG)


class BaseWorker(object):
    """
    Minimal worker implementation for python
    """

    def __init__(self,
                 endpoint,
                 description,
                 parameters,
                 id,
                 router,
                 collector,
                 receiver,
                 sender=SEND_PORT,
                 monitor=MONITOR_PORT,
                 result_server=RESULT_SERVER_LOCATION,
                 redis_server=REDIS_SERVER_LOCATION):

        self.redis_conn = redis.Redis(redis_server, 6379)

        self.id = id
        self.router = router
        self.result_file_server = result_server
        
        # 0MQ context
        context = zmq.Context()

        registered = self.redis_conn.hgetall('endpoints')
        if endpoint not in registered.keys():
            self.redis_conn.hset('endpoints', endpoint, receiver)
            self.redis_conn.hset(endpoint, 'description', str(description))

            serialized_params = json.dumps(parameters)
            self.redis_conn.hset(endpoint, 'parameters', serialized_params)

            logging.info('Service registered: ' + endpoint + ', Port ' + str(receiver))
        else:
            logging.debug('No need to register: ' + str(endpoint))

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
            'worker_id': str(self.id),
            'status': 'running'
        }
        return status

    def listen(self):
        # Start listening...
        logging.info('Worker: ID = ' + str(self.id) + ', Location = ' + str(self.router))

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
            logging.info('Data location => ' + str(data_location))

            response = client.get(data_location)

            input_data = response.json()
            input_dict = json.loads(input_data)

            final_result = self.run(data=input_dict)

            req = client.post(self.result_file_server + 'data', json=final_result, stream=True)
            file_id = req.json()['fileId']

            logging.debug('# Result saved to server = ' + str(req.json()))

            result = {
                'worker_id': str(self.id),
                'job_id': jid,
                'result': self.result_file_server + 'data/' + str(file_id)
            }

            # Send results to sink
            self.__sender.send_json(result)

    def run(self, data):
        pass

    def post_process(self, result, result_location):
        pass
