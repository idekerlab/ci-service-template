# -*- coding: utf-8 -*-
import zmq
import logging
import redis

REDIS_PORT = 6379
PULL_PORT = 6666 # For getting status message from other components

TAG_STATUS = 'status'
TAG_JOB_ID = 'job_id'

logging.basicConfig(level=logging.DEBUG)


class StatusMonitor():

    def __init__(self, pull=PULL_PORT, redisp=REDIS_PORT):
        # Prepare queue
        context = zmq.Context()

        # Socket to receive status messages on
        self.__receiver = context.socket(zmq.PULL)
        self.__receiver.bind("tcp://*:" + str(pull))

        # Connection to Redis server - host will be given from Docker-compose
        self.__redis_connection = redis.Redis(host='redis', port=redisp, db=0)

    def __set_status(self, message):
        job_id = message[TAG_JOB_ID]
        status = message[TAG_STATUS]
        self.__redis_connection.hset(name=TAG_STATUS, key=job_id, value=status)

        test = self.__redis_connection.hget(name=TAG_STATUS, key=job_id)
        logging.info('Job status updated: ' + str(test))

    def listen(self):
        logging.info('# Status Monitor starts: ' + str())

        while True:
            # Process any waiting tasks
            s = self.__receiver.recv_json()
            self.__set_status(s)


if __name__ == '__main__':
    status_monitor = StatusMonitor()
    status_monitor.listen()
