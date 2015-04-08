#!/bin/bash

# Run worker threads: In this example, running 4 workers.
rqworker --url redis://redis:6379/ &
rqworker --url redis://redis:6379/ &
rqworker --url redis://redis:6379/ &
rqworker --url redis://redis:6379/ &

# Run REST API server
python service.py