import logging
import redis

from flask.ext.restful import Resource, reqparse
from hdsubnetfinder.subnetwork.sub_network_finder import SubNetworkFinder
from hdsubnetfinder.kernel.kernel_generator import KernelGenerator
import hdsubnetfinder.subnetwork.network_util as util

from . import finders


class SubnetFinderResource(Resource):
    """
    List of available services.
    """

    def __init__(self):
        self.__redis_conn = redis.Redis('redis', 6379)
        self.parser = reqparse.RequestParser()

    def get(self):
        logging.debug('Listing available finders')

        registered_kernels = self.__redis_conn.hgetall()

        if registered_kernels is None:
            return [], 200

        kernels = []

        for key in registered_kernels.keys():
            service = {
                'networkLocation': key,
                'kernelLocation': str(registered_kernels[key])
            }
            kernels.append(service)

        return kernels, 200

    def post(self):

        self.parser.add_argument(
            'name',
            type=str,
            required=True,
            help='Name of this finder'
        )

        self.parser.add_argument(
            'kernel_url',
            type=str,
            required=True,
            help='Kernel file url'
        )

        self.parser.add_argument(
            'network_url',
            type=str,
            required=True,
            help='Network file url'
        )

        data = self.parser.parse_args()
        logging.debug('========== Finder data =========')
        logging.debug(data)

        kernel_file_url = data['kernel_url']
        network_file_url = data['network_url']
        name = data['name']

        generator = KernelGenerator()
        kernel = generator.create_kernel_from_file(kernel_file_url)
        network = util.read_sif(network_file_url)
        finder = SubNetworkFinder(kernel=kernel, network=network)

        finders[name] = finder

        logging.debug('========== Finder created =========')

        return {'message': 'Finder ' + name + ' created.'}, 200
