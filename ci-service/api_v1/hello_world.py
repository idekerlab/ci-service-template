from flask.ext import restful
from jobs import q, job_list
import time


class HelloService(restful.Resource):
    """
    Toy example to learn how to implement yo
    """

    def post(self):
        # Send the time-consuming job to workers
        name = 'John'
        job = q.enqueue_call(func=self.greet, args=(name,), result_ttl=6000)
        job_list.append(job.get_id())

        result = {
            'job_id': job.get_id(),
            'status': job.get_status()
        }

        return result, 202

    # Essentially, implementing new service means adding function like this.
    def greet(self, name):
        """
        Returns greeting message after 20 seconds.

        :param name: Name of the person
        :return: Greeting message
        """

        # Sleep for 20 seconds to emulate long-running task
        time.sleep(20)
        return 'Hello ' + name + '!'