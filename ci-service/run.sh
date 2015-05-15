#!/bin/bash

# Run worker threads: In this example, running 4 workers.
num_workers=4

for ((i=1; i<=$num_workers; i++)) {
	rqworker --url redis://redis:6379/ &
}

# Create temp result file directory
mkdir api_v1/utils/results

# Run REST API server
python service.py