# -*- coding: utf-8 -*-

from flask.ext.restful import Resource
import zmq
import redis


# Port for fetching task status
FETCH_PORT = 5555

# Port for status monitor
STATUS_PORT = 7777

REDIS_PORT = 6379

TAG_STATUS = 'status'
TAG_JOB_ID = 'job_id'


class TaskQueue(Resource):
    """
    API for job management.
    """

    def __init__(self, fetch=FETCH_PORT, status=STATUS_PORT, redisp=REDIS_PORT):
        super(TaskQueue, self).__init__()
        self.__redis_connection = redis.Redis(host='redis', port=redisp, db=0)

    def __get_status(self):
        status_hash = self.__redis_connection.hgetall(name=TAG_STATUS)
        serializable = []
        keys = status_hash.keys()

        for key in keys:
            serializable.append(
                {
                    TAG_JOB_ID: key.decode("utf-8"),
                    TAG_STATUS: status_hash[key].decode("utf-8")
                }
            )
        return serializable

    def get(self):
        status_message = self.__get_status()
        return status_message, 200

    def delete(self):
        """
        Delete all jobs
        :return:
        """
        return 200
