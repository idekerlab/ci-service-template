# -*- coding: utf-8 -*-
import zmq
import logging

import redis


class PortManager():

    def __init__(self, flaskapi, flaskapp, regport=9999):
        self.__api = flaskapi
        self.__app = flaskapp
        self.__regport = regport
        self.__redis_conn = redis.Redis('redis', 6379)

    def listen(self):
        context = zmq.Context()

        # For accept new worker
        # Listening to assign new port for the new worker
        self.__register = context.socket(zmq.PULL)
        url = 'tcp://*:' + str(self.__regport)
        self.__register.bind(url)

        while True:
            new_worker = self.__register.recv_json()
            logging.info('New Worker instance: ' + str(new_worker))

            endpoint = new_worker['endpoint']
            port_number = new_worker['port_number']

            registered = self.__redis_conn.hgetall('endpoints')
            if endpoint not in registered.keys():
                self.__redis_conn.hset('endpoints', endpoint, port_number)
                logging.info('Service registered: ' + endpoint + ', Port ' + str(port_number))
