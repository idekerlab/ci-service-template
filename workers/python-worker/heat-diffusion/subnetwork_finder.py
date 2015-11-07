import logging

from ciworker.base_worker import BaseWorker
from hdsubnetfinder.subnetwork.sub_network_finder import SubNetworkFinder
from hdsubnetfinder.kernel.kernel_generator import KernelGenerator
import hdsubnetfinder.subnetwork.network_util as util


class SubnetworkFinderWorker(BaseWorker):

    __finders = {}

    def run(self, data):

        logging.debug('Worker ID: ' + str(self.id) + ' Building finder '
                                                     '=========')
        logging.debug(data)

        kernel_file_url = data['kernel_url']
        network_file_url = data['network_url']
        query = data['query']

        # Check finder exists or not
        if kernel_file_url in self.__finders.keys():
            logging.debug('Kernel found.  No need to create finder')
            finder = self.__finders[kernel_file_url]
        else:
            logging.debug('Building Finder...')
            generator = KernelGenerator()
            kernel = generator.create_kernel_from_file(kernel_file_url)
            network = util.read_sif(network_file_url)
            finder = SubNetworkFinder(kernel=kernel, network=network)
            self.__finders[kernel_file_url] = finder
            logging.debug('Building Finder... Done!')

        # Now find subnet
        logging.debug('******** Query: ' + str(query))
        subnetwork = finder.get_sub_network(query)
        logging.debug('========== Sub Network found: Size = ' + str(len(
            subnetwork)))

        return subnetwork
