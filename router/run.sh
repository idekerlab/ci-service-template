#!/bin/bash

# IP Address of the router
router_ip='10.0.1.17'
router_port=5557

echo 'Starting Collector...'

python ./zmqrouter/collector.py