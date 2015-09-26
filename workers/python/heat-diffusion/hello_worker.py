from base_worker import BaseWorker

import time
import arg_parser as parser

class HelloWorker(BaseWorker):

    def run(self, data):
        # Parse input data
        msg = data['message']
        time.sleep(5)

        new_message = 'Hello ' + str(msg)
        greeting = {
            'message': new_message
        }

        return greeting


if __name__ == '__main__':
    args = parser.get_args()

    hello_worker = HelloWorker(
        endpoint=args.endpoint,
        id=args.id,
        router=args.router,
        collector=args.collector,
        receiver=args.port)

    hello_worker.listen()