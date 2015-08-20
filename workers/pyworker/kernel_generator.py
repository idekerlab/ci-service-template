# -*- coding: utf-8 -*-
import logging
import uuid
import requests as client
import arg_parser as parser

from base_worker import BaseWorker
from hdsubnetfinder.kernel.kernel_generator import KernelGenerator
import hdsubnetfinder.kernel.kernel_util as util

KERNEL_FILE_SERVER = 'http://kernelserver:3000/'


class KernelGeneratorWorker(BaseWorker):

    def run(self, data):
        # Parse input data
        sif_url = data['network_url']
        generator = KernelGenerator()
        kernel = generator.create_kernel(sif_url)
        logging.debug('========== Kernel computation finished =========')

        req = client.post(KERNEL_FILE_SERVER + 'data',
                          data=util.get_kernel_as_string(kernel), stream=True)
        file_id = req.json()['fileId']

        # Register kernel information
        kernel_id = str(uuid.uuid4())
        kernel_file_url = KERNEL_FILE_SERVER + 'data/' + file_id

        self.redis_conn.hset('kernels', kernel_id, kernel_file_url)
        self.redis_conn.hset('kernel2network', kernel_id, sif_url)

        logging.debug('Kernel File Server response Data = ' + str(req.json()))
        result = {
            'kernel_id': kernel_id,
            'network': sif_url,
            'kernel_file': kernel_file_url
        }

        return result


if __name__ == '__main__':
    args = parser.get_args()

    worker = KernelGeneratorWorker(
        endpoint=args.endpoint,
        id=args.id,
        router=args.router,
        collector=args.collector,
        receiver=args.port)

    worker.listen()
