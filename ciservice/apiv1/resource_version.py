# -*- coding: utf-8 -*-
import logging
from flask.ext.restful import Resource
from flask import request


class VersionResource(Resource):
    """Simple service information API
    Simply displays information about this API server.
    This will be used to check whether the service is actually working or not.
    """

    def get(self):
        logging.debug('GET called for Version resource')

        version = {
            'serviceName': 'Cytoscape CI template service',
            'version': '1',
            'message': 'Called by:  ' + str(request.remote_addr)
        }

        return version, 200
