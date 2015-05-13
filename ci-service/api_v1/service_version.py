# -*- coding: utf-8 -*-

"""Simple service information API
Simply displays information about this API.
This will be used to check whether the service is actually working or not.
"""

from flask.ext import restful
from flask import request
from . import task_logger as logger


class Version(restful.Resource):
    """
    API to display basic service information.
    """

    def get(self):

        # This is standard logger in Flask
        logger.debug('GET called for Version API')

        version = {
            'serviceName': 'Cytoscape CI template service',
            'version': '1',
            'message': 'Called by:  ' + str(request.remote_addr)
        }

        return version, 200
