import time
from base_service import MemoryResultService
from utils.logger_factory import LoggerUtil

task_logger = LoggerUtil.get_logger(__name__)


class HelloService(MemoryResultService):
    """
    Task example: Return posted data after 10 seconds.
    """

    def parse_args(self):
        self.parser.add_argument('name', type=str, required=True, help='Your name')

    def run_service(self, data):
        task_logger.debug('Hello service start')

        # Sleep for 10 seconds to emulate long-running task
        time.sleep(10)
        greet = {
            'message': 'Hello ' + data['name'] + '!'
        }
        return greet
