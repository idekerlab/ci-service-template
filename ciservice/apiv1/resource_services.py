# -*- coding: utf-8 -*-
import redis

from flask.ext.restful import Resource
from util_service import ServiceUtil


class ServicesResource(Resource):
    """
    List of available services.
    """

    def __init__(self):
        self.__redis_conn = redis.Redis('redis', 6379)
        self.__util = ServiceUtil()

    def get(self):
        """
        List all registered services.
        :return:
        """
        registered_services = self.__redis_conn.hgetall('endpoints')
        services = []

        for key in registered_services.keys():
            services.append(self.__util.get_service_details(key))

        return services, 200
