# -*- coding: utf-8 -*-
import zmq
import logging
import redis


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


        self.__redis_connection = redis.Redis(host='redis', port=6379, db=0)
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

                    self.__redis_connection.set(job_id, status) 

                    logging.info('Redis: Current status = ' 
                        + str(self.__redis_connection.get(job_id)))

                    for key in self.__redis_connection.scan_iter():
                        logging.info(str(key) + 
                            str(self.__redis_connection.get(str(key))))

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
