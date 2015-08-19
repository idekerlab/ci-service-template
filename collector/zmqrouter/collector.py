import zmq
import logging
import redis

RESULT_DIR = '/collector/jobs'
MONITOR_PORT = 6666
COLLECTOR_PORT = 5558

logging.basicConfig(level=logging.DEBUG)


class Collector():

    def __init__(self, redisp=6379):
        context = zmq.Context()

        # Socket to receive result
        self.__receiver = context.socket(zmq.PULL)
        self.__receiver.bind("tcp://*:" + str(COLLECTOR_PORT))

        # Connect to monitor process
        self.__monitor = context.socket(zmq.PUSH)
        self.__monitor.connect('tcp://127.0.0.1:' + str(MONITOR_PORT))

        self.__redis_connection = redis.Redis(host='redis', port=redisp, db=0)

    def listen(self):
        logging.info('#### Collector is listening on: ' + str(COLLECTOR_PORT))

        while True:
            s = self.__receiver.recv_json()
            logging.info('######## Collector gets message #########')
            logging.info(str(s))

            job_id, result = self.__save_result(s)

            # Send status to monitor
            status_update = {
                'job_id': job_id,
                'result': result,
                'status': 'finished'
            }

            logging.info('######## Message #########')
            logging.info(str(s))
            self.__monitor.send_json(status_update)

    def __save_result(self, data):
        # Save the result to file.
        job_id = data['job_id']
        result = data['result']

        self.__redis_connection.hset(name='results', key=job_id, value=result)

        return job_id, result


if __name__ == '__main__':
    collector = Collector()
    collector.listen()
