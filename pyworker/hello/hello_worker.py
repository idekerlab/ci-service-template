import time
from base.base_worker import BaseWorker
from base import arg_parser as parser


class HelloWorker(BaseWorker):

    def __init__(self, endpoint, id, router, collector, receiver):

        description = 'Sample service returning message.'
        parameters = {
            "message": {
                "type": "string",
                "description": "Any string message to be returned.",
                "required": True
            }
        }

        super(HelloWorker, self).__init__(endpoint, description,
                                          parameters, id, router,
                                          collector, receiver)

    def run(self, data):
        # Check required parameters
        if 'message' not in data.keys():
            return {'error': 'message parameter is missing.'}

        # Extract input parameter and create return value
        greeting = {'message': 'Hello ' + str(data['message'])}

        # Sleep to emulate time consuming task...
        time.sleep(5)

        # Return result as object
        return greeting


if __name__ == '__main__':
    args = parser.get_args()

    hello_worker = HelloWorker(
        endpoint=args.endpoint,
        id=args.id,
        router=args.router,
        collector=args.collector,
        receiver=args.port
    )

    hello_worker.listen()
