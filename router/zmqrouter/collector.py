import sys
import zmq
import logging

# Collector


class Collector():

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        context = zmq.Context()
        # Socket to receive messages on
        self.__receiver = context.socket(zmq.PULL)
        self.__receiver.bind("tcp://*:5558")

    def listen(self):
        while True:
            s = self.__receiver.recv_json()
            self.__save_result(s)

    def __save_result(self, data):
        # Save the result to file.
        jobid = data['job_id']
        logging.info('Job ' + str(jobid) + ' saved.')
        pass


if __name__ == '__main__':
    collector = Collector()
    collector.listen()
