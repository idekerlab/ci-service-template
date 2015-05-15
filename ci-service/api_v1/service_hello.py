import time
import logging

from base_service import MemoryResultService


class HelloService(MemoryResultService):
    """
    Task example: Return posted data after 10 seconds.
    """

    def parse_args(self):
        self.parser.add_argument('name', type=str, required=True, help='Your name')

    def run_service(self, data):

        logging.getLogger(__name__).debug('Hello service start...')

        # Sleep for 10 seconds to emulate long-running task
        time.sleep(10)

        greet = {
            'message': 'Hello ' + data['name'] + '!'
        }
        return greet
