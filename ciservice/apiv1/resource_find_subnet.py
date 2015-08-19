import logging
import redis

from flask import request
from flask.ext.restful import Resource, reqparse

from . import finders
import json

class FindSubnetResource(Resource):
    """
    List of available services.
    """

    def __init__(self):
        self.__redis_conn = redis.Redis('redis', 6379)

    def post(self, name):
        data = request.data
        finder = finders[name]

        logging.debug('========== Finder start =========')
        logging.debug(finder)
        logging.debug(data)
        parsed = json.loads(data)
        logging.debug(parsed)

        query = parsed['query']
        logging.debug('Query: ========= ' + str(query))
        result = finder.get_sub_network(query)
        logging.debug('========== Subnetwork found: ' + str (len(result)))

        return result, 200
