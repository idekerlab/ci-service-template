from flask import Flask
from flask.ext import restful

from api_v1.graph_analysis import *
from api_v1.version import *
from api_v1.jobs import *
from api_v1.job import *
from api_v1.hello_world import *

from api_v1.file_streaming import *

app = Flask(__name__)
api = restful.Api(app)

# Top-level URL - simply returns service name
api.add_resource(Version, '/v1')

# Toy example to return greeting message.
api.add_resource(HelloService, '/v1/hello')

api.add_resource(StreamingService, '/v1/jobs/<job_id>/result')

# Sample services: Calculate graph statistics
api.add_resource(Betweenness, '/v1/algorithms/betweenness')
api.add_resource(PageRank, '/v1/algorithms/pagerank')
api.add_resource(Clustering, '/v1/algorithms/clustering')

# Task Queue
api.add_resource(Jobs, '/v1/jobs')
api.add_resource(SingleJob, '/v1/jobs/<job_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
