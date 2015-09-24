#!/bin/bash

# IP Address of the router
echo 'Starting Collector and Monitor...'

# Temp dir for result files
mkdir /collector/jobs

# Task monitor
python ./zmqrouter/status_monitor.py &

# Result collector
python ./zmqrouter/collector.py
