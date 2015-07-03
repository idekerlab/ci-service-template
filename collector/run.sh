#!/bin/bash

# IP Address of the router
echo 'Starting Collector and Monitor...'

mkdir /collector/jobs

python ./zmqrouter/status_monitor.py &

python ./zmqrouter/collector.py