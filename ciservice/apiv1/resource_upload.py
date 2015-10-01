# -*- coding: utf-8 -*-
import logging
import requests as rqc
from flask.ext.restful import Resource
from flask import Response, request
from flask import stream_with_context

INPUT_DATA_SERVER_LOCATION = 'http://dataserver:3000/'


class UploadResource(Resource):

    def get(self):
        req = rqc.get(INPUT_DATA_SERVER_LOCATION, stream=True)
        return Response(
            stream_with_context(req.iter_content()),
            content_type=req.headers['content-type']
        )

    def post(self):
        """
        Stream input to data file server.
        :return:
        """
        logging.debug('UPLOAD POST')

        req = rqc.post(INPUT_DATA_SERVER_LOCATION + 'data',
                       json=request.stream.read(),
                       stream=True)

        return Response(
            stream_with_context(req.iter_content()),
            content_type=req.headers['content-type']
        )
