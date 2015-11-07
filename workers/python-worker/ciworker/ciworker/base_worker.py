import zmq
import logging
import json
import redis
import requests as client

logging.basicConfig(level=logging.DEBUG)


class BaseWorker(object):
    """
    Minimal worker implementation for python
    """

    def __init__(self, config, id):

        self.id = id
        endpoint = config['endpoint']
        description = config['description']

        # Setup servers
        servers = config['servers']

        config_redis = servers['redis']
        self.redis_conn = redis.Redis(
                config_redis['location'], config_redis['port'])

        config_task_queue = servers['task_queue']
        router = config_task_queue['location']
        router_port = config_task_queue['port']

        config_collector = servers['collector']
        collector = config_collector['location']
        collector_port = config_collector['port']

        config_monitor = servers['monitor']
        monitor = config_monitor['location']
        monitor_port = config_monitor['port']

        config_result = servers['result']
        result_file_server = config_result['location']
        result_file_server_port = config_result['port']

        self.result_server = 'http://' + result_file_server + ':' \
                             + str(result_file_server_port) + '/'

        # API Parameters
        parameters = config['parameters']

        # 0MQ context
        context = zmq.Context()

        registered = self.redis_conn.hgetall('endpoints')
        if endpoint not in registered.keys():
            logging.debug('!!!!!!!!!!!! register: ' + str(endpoint))

            self.redis_conn.hset('endpoints', endpoint, router_port)
            self.redis_conn.hset(endpoint, 'description', str(description))

            serialized_params = json.dumps(parameters)
            self.redis_conn.hset(endpoint, 'parameters', serialized_params)

            logging.info('Service registered: ' + endpoint + ', Port '
                         + str(router_port))
        else:
            logging.debug('No need to register: ' + str(endpoint))

        # For getting input data for this worker
        self.__receiver = context.socket(zmq.PULL)
        self.__receiver.connect('tcp://' + router + ':' + str(router_port))

        # For sending out the result to collector
        self.__sender = context.socket(zmq.PUSH)
        self.__sender.connect('tcp://' + collector + ':' + str(collector_port))

        # for status monitoring
        self.__monitor = context.socket(zmq.PUSH)
        self.__monitor.connect('tcp://' + monitor + ':' + str(monitor_port))

    def __create_status(self, job_id):
        status = {
            'job_id': job_id,
            'worker_id': str(self.id),
            'status': 'running'
        }
        return status

    def listen(self):
        # Start listening...
        logging.info('Python Worker: ID = ' + str(self.id))

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

            try:
                response = client.get(data_location)
            except:
                # Error happened while getting input data
                result = {
                    'worker_id': str(self.id),
                    'job_id': jid,
                    'result': 'failed!'
                }
                self.__sender.send_json(result)

            input_data = response.json()
            input_dict = json.loads(input_data)

            # Run the service code.  This is the actual function of this
            # service.
            final_result = self.run(data=input_dict)

            req = client.post(self.result_server + 'data', data=final_result,
                              stream=True)
            file_id = req.json()['fileId']

            logging.debug('# Result saved to server = ' + str(req.json()))

            result = {
                'worker_id': str(self.id),
                'job_id': jid,
                'result': self.result_server + 'data/' + str(file_id)
            }

            # Send results to sink
            self.__sender.send_json(result)

    def run(self, data):
        pass

    def post_process(self, result, result_location):
        pass
