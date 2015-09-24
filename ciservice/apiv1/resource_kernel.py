import logging
import redis

from flask.ext.restful import Resource

KERNELS_TAG = 'kernels'

class KernelResource(Resource):
    """
    List of available services.
    """

    def __init__(self):
        self.__redis_conn = redis.Redis('redis', 6379)

    def get(self):
        logging.debug('Listing available kernels')

        registered_kernels = self.__redis_conn.hgetall(KERNELS_TAG)

        if registered_kernels is None:
            return [], 200

        kernels = []

        for key in registered_kernels.keys():
            service = {
                'kernelId': key,
                'networkSource': str(registered_kernels[key])
            }
            kernels.append(service)

        return kernels, 200
