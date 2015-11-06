import time
from ciworker.base_worker import BaseWorker


class HelloWorker(BaseWorker):
    """
    The most basic 'hello world' service example.
    This service simply takes message from the caller
    and add Hello in front of the sentence.
    """

    def run(self, data):
        """
        Actual service call.

        :param data: dictionary of message.  It should have
         'message' as the key.
        :return:
        """

        if 'message' not in data.keys():
            return {
                'error': 'message parameter is missing.'
            }

        # Extract input parameter and create return value
        greeting = {'message': 'Hello ' + str(data['message'])}

        # Sleep to emulate time consuming task...
        time.sleep(3)

        # Return result as object
        return greeting
