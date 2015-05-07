from api_v1 import api, app

from api_v1.service_version import Version
from api_v1.jobs import *
from api_v1.job import *

from api_v1.service_hello import *
from api_v1.service_graph_analysis import *
from api_v1.service_graph_generator import *

# Top-level URL - simply returns service name
api.add_resource(Version, '')

# Toy example to return greeting message.
api.add_resource(HelloService, '/hello')

# Sample services: Calculate graph statistics
api.add_resource(Betweenness, '/algorithms/betweenness')
api.add_resource(PageRank, '/algorithms/pagerank')
api.add_resource(Clustering, '/algorithms/clustering')

# Sample services: Using temp files for results
api.add_resource(ScaleFree, '/generators/scalefree')

# Task Queue
api.add_resource(Jobs, '/jobs')
api.add_resource(SingleJob, '/jobs/<job_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
