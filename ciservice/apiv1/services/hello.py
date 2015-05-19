import logging
import time


class HelloService():
    @staticmethod
    def say_hello(data):
        """
        Example service to return greet massage using
        'name' text in the data object

        :param data: data object contains name
        :return: greet message as dict
        """
        logging.debug('Hello service start...')

        # Sleep for 10 seconds to emulate long-running task
        time.sleep(10)

        greet = {
            'message': 'Hello ' + data['name'] + '!'
        }
        return greet
