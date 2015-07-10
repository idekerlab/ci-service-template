# -*- coding: utf-8 -*-
import zmq
import logging
import redis

logging.basicConfig(level=logging.DEBUG)

REDIS_PORT = 6379

PULL_PORT = 6666
PUSH_PORT = 7777 # for sending back the result


class StatusMonitor():

    def __init__(self, push=PUSH_PORT, pull=PULL_PORT,
                 redisp=REDIS_PORT):
        # Prepare queue
        context = zmq.Context()
        # Socket to receive messages on
        self.__receiver = context.socket(zmq.PULL)
        self.__receiver.bind("tcp://*:" + str(pull))

        # For sending back results
        self.__sender = context.socket(zmq.REP)
        self.__sender.bind("tcp://*:" + str(push))

        # Connection to Redis server - host will be given from Docker-compose
        # This will be used only for storing status.
        self.__redis_connection = redis.Redis(host='redis', port=redisp, db=0)

        # TODO: remove this - List of jobs
        self.jobs = {}
        logging.info('Task monitor initialized')


    def __get_status(self):
        # status is saved in a hash.  Simple call the hash object
        # from redis.
        status_hash = self.__redis_connection.hgetall(name='status')
        serializable = []
        for key in status_hash.keys():
            serializable.append({
                'job_id': key.decode("utf-8"),
                'status': status_hash[key].decode("utf-8")
            })
        return serializable



    def __set_status(self, message):
        """Set status of the job to Redis DB
        :return:
        """
        job_id = message['job_id']
        status = message['status']
        self.__redis_connection.hset(name='status', key=job_id, value=status)

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

                    self.__set_status(s)
                    logging.info('Redis: Current status = ' 
                        + str(self.__redis_connection.hget(name='status', key=job_id)))

                except zmq.Again:
                    break

            while True:
                try:
                    s = self.__sender.recv_json(zmq.DONTWAIT)
                    logging.info('** New message = ' + str(s))
                    status_list = self.__get_status()
                    logging.info('** status = ' + str(status_list))
                    self.__sender.send_json(status_list)
                except zmq.Again:
                    break


if __name__ == '__main__':

    status_monitor = StatusMonitor()
    status_monitor.listen()
