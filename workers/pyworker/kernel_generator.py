# -*- coding: utf-8 -*-
import logging
import arg_parser as parser

from base_worker import BaseWorker
from hdsubnetfinder.kernel.kernel_generator import KernelGenerator
import hdsubnetfinder.kernel.kernel_util as util


class KernelGeneratorWorker(BaseWorker):

    def run(self, data):
        # Parse input data
        sif_url = data['network_url']
        generator = KernelGenerator()
        kernel = generator.create_kernel(sif_url)
        logging.debug('========== Kernel computation finished =========')

        # Create file from this
        util.write_kernel(kernel, output_file='temp.kernel.txt')

        kernel_array = []
        counter=0

        for line in open('temp.kernel.txt', 'r'):
            counter += 1
            logging.debug('###2 LINE: ' + str(counter))
            kernel_array.append(line)

        return ''.join(kernel_array)


if __name__ == '__main__':
    args = parser.get_args()

    worker = KernelGeneratorWorker(
        endpoint=args.endpoint,
        id=args.id,
        router=args.router,
        collector=args.collector,
        receiver=args.port)

    worker.listen()
