from flask.ext import restful
from jobs import q, job_list
from flask.ext.restful import reqparse
import time

from . import logger


class HelloService(restful.Resource):
    """
    Simple service example to use task queue.
    """

    def __init__(self):
        """
        Initialize request parameter parser

        :return:
        """

        self.__parser = reqparse.RequestParser()

    def get(self):
        """Return simple message about this service

        :return:
        """

        # Use this logger for debug messages.
        logger.debug('GET called for /hello')

        description = {
            'message': 'Greet service.  Use POST to test queue.'
        }

        return description, 200

    def post(self):
        """Return a greet message

        Document body should have name.

        :return: Job status
        """

        self.__parser.add_argument('name', type=str, help='Your name')
        name = self.__parser.parse_args()

        # Send the time-consuming job to workers
        job = q.enqueue_call(func=self.greet, args=(name,), result_ttl=6000)
        job_list.append(job.get_id())

        result = {
            'job_id': job.get_id(),
            'status': job.get_status()
        }

        return result, 202

    def greet(self, name):
        """Returns greeting message string after 20 seconds.

        :param name: Name of the person

        :return: Greeting message
        """

        # Sleep for 20 seconds to emulate long-running task
        time.sleep(20)

        return 'Hello ' + name + '!'