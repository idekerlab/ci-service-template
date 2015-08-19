#!/bin/bash

# Run workers for 0MQ

new_workers=2

kernel_endpoint='kernel'
subnet_endpoint='subnet'

# IP Address of the router
router_ip='service'
collector_ip='collector'

kernel_router_port=5556
subnet_router_port=5557

collector_port=5558

for ((i=1; i<=$new_workers; i++)) {
	python kernel_generator.py $kernel_endpoint $i $router_ip $collector_ip \
		$kernel_router_port &

	python subnetwork_finder.py $subnet_endpoint $i $router_ip $collector_ip \
		$subnet_router_port &
}

python subnetwork_finder.py $subnet_endpoint $i $router_ip $collector_ip \
		$subnet_router_port

