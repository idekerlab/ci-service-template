# -*- coding: utf-8 -*-

import zmq

import logging

logging.basicConfig(level=logging.DEBUG)
logging.info('-------------------------')

context = zmq.Context(1)

# Socket facing clients
frontend = context.socket(zmq.XREP)
frontend.bind("tcp://*:5556")


# Socket facing services
backend = context.socket(zmq.XREQ)
backend.bind("tcp://*:5558")

logging.info('Starting-------------------------')


zmq.device(zmq.QUEUE, frontend, backend)

