from flask import Response
from flask import Flask
import json
import os
from flask_restful import Resource, Api

import logging

# Simply stream files from local file system.

app = Flask(__name__)
api = Api(app)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class Streamer(Resource):
    """
    Simply stream the result file.
    """

    # TODO: test performance for GB+ files
    def get(self, job_id):

        def generate_file(job_id):
            f = open('/collector/jobs/' + str(job_id))
            for row in f:
                yield row

        return Response(generate_file(job_id))


api.add_resource(Streamer, '/results/<string:job_id>')

@app.route('/')
def status():
    return json.dumps({'status': 'streamer is working'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
