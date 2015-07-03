# -*- coding: utf-8 -*-
import zmq
import logging


logging.basicConfig(level=logging.DEBUG)


class StatusMonitor():

    def __init__(self):
        context = zmq.Context()
        # Socket to receive messages on
        self.__receiver = context.socket(zmq.PULL)
        self.__receiver.bind("tcp://*:6666")

        # For sending back results
        self.__socket = context.socket(zmq.REP)
        self.__socket.bind("tcp://*:7777")

        # List of jobs
        self.jobs = {}
        logging.info('MONITOR start = ')

    def listen(self):
        while True:
            # Process any waiting tasks
            while True:
                try:
                    s = self.__receiver.recv_json(zmq.DONTWAIT)

                    if 'status' not in s.keys():
                        continue

                    job_id = s['job_id']
                    status = s['status']
                    self.jobs[job_id] = status
                    logging.info('Current status = ' + str(self.jobs))

                except zmq.Again:
                    break

            while True:
                try:
                    s = self.__socket.recv_json(zmq.DONTWAIT)
                    logging.info('** New message = ' + str(s))
                    self.__socket.send_json(self.jobs)
                except zmq.Again:
                    break


if __name__ == '__main__':

    status_monitor = StatusMonitor()
    status_monitor.listen()
