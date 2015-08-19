import logging
import uuid
import arg_parser as parser

from base_worker import BaseWorker
from hdsubnetfinder.subnetwork.sub_network_finder import SubNetworkFinder
from hdsubnetfinder.kernel.kernel_generator import KernelGenerator


class SubnetworkFinderWorker(BaseWorker):

    def run(self, data):
        # Parse input data
        kernel_file_url = data['kernel_url']
        network_file_url = data['network_url']

        generator = KernelGenerator()
        kernel = generator.create_kernel_from_file(kernel_file_url)

        finder = SubNetworkFinder(kernel, network_file_url)
        logging.debug('========== Finder created =========')

        # Register kernel information

        self.redis_conn.hset('kernels', str(uuid.uuid4()), sif_url)

        # Create file from this
        util.write_kernel(kernel, output_file='temp.kernel.txt')

        kernel_array = []
        counter = 0

        for line in open('temp.kernel.txt', 'r'):
            counter += 1
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
