#!/bin/bash

#
# Run script for R workers.
#

# Number of workers to be created
new_workers=2

# IP Address of the router
router_ip='service'
collector_ip='collector'
router_port=8888
collector_port=5558

echo 'Starting R workers...'

for ((i=1; i<=$new_workers; i++)) {
	Rscript ./worker.R $router_ip $collector_ip $router_port $collector_port &
}

Rscript ./worker.R $router_ip $collector_ip $router_port $collector_port
