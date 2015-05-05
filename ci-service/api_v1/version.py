# -*- coding: utf-8 -*-

"""Simple service information API
Simply displays information about this API.
This will be used to check whether the service is actually working or not.
"""

from flask.ext import restful
from flask.ext.restful import reqparse
from flask import request
from flask import jsonify


class Version(restful.Resource):
    """
    API to display basic service information.
    """

    def __init__(self):
        self.__parser = reqparse.RequestParser()

    def get(self):
        version = {
            'serviceName': 'Cytoscape CI template service',
            'version': '0.1.1',
            'message': 'Called from: ' + str(request.remote_addr)
        }

        return version, 200