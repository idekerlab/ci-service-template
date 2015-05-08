from flask.ext import restful
from flask.ext.restful import reqparse

# Lifetime of the results.
RESULT_TIME_TO_LIVE = 500000


class EchoService(restful.Resource):
    """
    Echo server to return POST body
    """

    def __init__(self):
        self.__parser = reqparse.RequestParser()

    def post(self):
        """
        Create and submit a new graph analysis job in the queue.
        :return:
        """

        # Extract data from body of POST call
        self.__parser.add_argument('args', action='append', help='arguments')
        args = self.__parser.parse_args()

        # Job created.
        return args, 202
