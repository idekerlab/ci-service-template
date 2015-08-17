# -*- coding: utf-8 -*-
import logging
import arg_parser as parser
import cStringIO

from base_worker import BaseWorker
from kernel.kernel_generator import KernelGenerator

class KernelGeneratorWorker(BaseWorker):

    def run(self, data):
        # Parse input data
        sif_url = data['network_url']
        generator = KernelGenerator(sif_url)
        output = cStringIO.StringIO()
        kernel = generator.write_kernel(output)
        output.close()
        logging.debug('Kernel computation finished.')

        return kernel


if __name__ == '__main__':
    args = parser.get_args()

    worker = KernelGeneratorWorker(
        endpoint=args.endpoint,
        id=args.id,
        router=args.router,
        collector=args.collector,
        receiver=args.port)

    worker.listen()
