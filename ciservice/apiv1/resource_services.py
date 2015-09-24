# -*- coding: utf-8 -*-

import logging
import redis

from flask.ext.restful import Resource


class ServicesResource(Resource):
    """
    List of available services.
    """

    def __init__(self):
        self.__redis_conn = redis.Redis('redis', 6379)

    def get(self):
        logging.debug('Listing available services')

        registered_services = self.__redis_conn.hgetall('endpoints')

        services = []

        for key in registered_services.keys():
            service = {
                'serviceName': key,
                'portNumber': str(registered_services[key])
            }
            services.append(service)

        return services, 200
