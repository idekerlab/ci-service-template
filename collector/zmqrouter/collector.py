import zmq
import logging
import os
import json

RESULT_DIR = '/collector/jobs'
MONITOR_PORT = 6666

logging.basicConfig(level=logging.DEBUG)


class Collector():

    def __init__(self, job_dict):
        context = zmq.Context()
        # Socket to receive messages on
        self.__receiver = context.socket(zmq.PULL)
        self.__receiver.bind("tcp://*:5558")

        # For sending back results
        self.__socket = context.socket(zmq.REP)
        self.__socket.bind("tcp://*:5555")

        self.__monitor = context.socket(zmq.PUSH)
        self.__monitor.connect('tcp://127.0.0.1:' + str(MONITOR_PORT))

        # List of jobs
        self.jobs = job_dict

    def listen(self):
        while True:
            # Process any waiting tasks
            while True:
                try:
                    s = self.__receiver.recv_json(zmq.DONTWAIT)

                    if 'result' not in s.keys():
                        continue

                    job_id = self.__save_result(s)
                    logging.info('# result = ' + str(len(self.jobs)))

                    # Send status to monitor
                    status_update = {
                        'job_id': job_id,
                        'status': 'finished'
                    }
                    self.__monitor.send_json(status_update)
                except zmq.Again:
                    break

            while True:
                try:
                    s = self.__socket.recv_json(zmq.DONTWAIT)
                    logging.info('** New message = ' + str(s))
                    self.__socket.send_json(self.jobs)
                except zmq.Again:
                    break

    def __save_result(self, data):
        # Save the result to file.
        job_id = data['job_id']
        result = data['result']
        self.__write_data(result, job_id)
        return job_id

    def __write_data(self, data, job_id):
        filename = os.path.join(RESULT_DIR, job_id)

        temp_file = open(filename, 'w')
        json.dump(data, temp_file, indent=2)
        temp_file.close()
        self.jobs[job_id] = filename


    def get_result(self):
        pass

    def __delete_data(self, job_id):
        pass


if __name__ == '__main__':

    job_dict = {}
    collector = Collector(job_dict)
    collector.listen()
