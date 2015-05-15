# -*- coding: utf-8 -*-

"""Simple service information API
Simply displays information about this API.
This will be used to check whether the service is actually working or not.
"""

from flask.ext.restful import Resource
from flask import request
import logging


class Version(Resource):
    """
    API to display basic service information.
    """

    def get(self):

        logging.getLogger(__name__).debug('GET called for Version API')

        version = {
            'serviceName': 'Cytoscape CI template service',
            'version': '1',
            'message': 'Called by:  ' + str(request.remote_addr)
        }

        return version, 200
