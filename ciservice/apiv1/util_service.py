# -*- coding: utf-8 -*-
import redis
import json


class ServiceUtil():

    def __init__(self):
        self.__redis_conn = redis.Redis('redis', 6379)

    def get_service_details(self, service_name):
        port_number = self.__redis_conn.hget('endpoints', key=service_name)
        desc = self.__redis_conn.hget(service_name, 'description')
        params = self.__redis_conn.hget(service_name, 'parameters')
        param_object = json.loads(params)

        service_details = {
            'serviceName': service_name,
            'description': desc,
            'portNumber': str(port_number),
            'parameters': param_object
        }

        return service_details
