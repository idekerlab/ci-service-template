# -*- coding: utf-8 -*-
# Router for ZMQ tasks.
#

import zmq
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug('============ Initializing router... =============')

context = zmq.Context()
frontend = context.socket(zmq.ROUTER)
backend = context.socket(zmq.DEALER)


import socket
logging.getLogger(__name__).debug(
    str(socket.gethostbyname('service')))
service_ip = socket.gethostbyname('service')


frontend.bind('tcp://*:5556')
backend.bind("tcp://*:5560")

# Initialize poll set
poller = zmq.Poller()
poller.register(frontend, zmq.POLLIN)
poller.register(backend, zmq.POLLIN)

logging.debug('=========== Router initialized ===================')

# Switch messages between sockets
while True:
    socks = dict(poller.poll())

    if socks.get(frontend) == zmq.POLLIN:
        data = frontend.recv_json()
        logging.debug('GOT data===================')
        #message = frontend.recv_multipart()
        #backend.send_multipart(message)

    if socks.get(backend) == zmq.POLLIN:
        message = backend.recv_multipart()
        frontend.send_multipart(message)
