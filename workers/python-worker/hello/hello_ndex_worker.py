# -*- coding: utf-8 -*-
import requests

from ciworker.base_worker import BaseWorker

NDEX_NETWORK_ENDPOINT = 'http://public.ndexbio.org/rest/network/'
NDEX_COMMAND_GET_COMPLETE_NET = '/asNetwork'


class HelloNdexWorker(BaseWorker):
    """
    Sample worker to call external service (NDEx).
    """

    def run(self, data):
        """
        Toy example to create SIF-like array from NDEx network
        :param data:
        :return:
        """

        if 'network_id' not in data.keys():
            return {
                'error': 'network_id is missing.'
            }

        # Get network data from NDEx
        network_id = str(data['network_id'])
        result = requests.get(NDEX_NETWORK_ENDPOINT + network_id + NDEX_COMMAND_GET_COMPLETE_NET)

        ndex_network = result.json()
        sif = self.ndex2sif(ndex_network)

        # Return result as object

        return sif

    def ndex2sif(self, ndex_network):
        sif_network = []

        edges = ndex_network['edges']

        for edge_id in edges.keys():
            edge = edges[edge_id]
            row = str(edge['objectId']) + ' ' + str(edge['predicateId']) \
                  + ' ' + str(edge['subjectId'])
            sif_network.append(row)

        return sif_network
