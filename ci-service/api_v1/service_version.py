# -*- coding: utf-8 -*-

"""Simple service information API
Simply displays information about this API.
This will be used to check whether the service is actually working or not.
"""

from flask.ext import restful
from flask import request

# For logging
from . import logger

VERSION = '0.2.0'


class Version(restful.Resource):
    """
    API to display basic service information.
    """

    def get(self):

        logger.debug('Version API GET method called.')

        version = {
            'serviceName': 'Cytoscape CI template service',
            'version': VERSION,
            'message': 'Called by:  ' + str(request.remote_addr)
        }

        return version, 200
