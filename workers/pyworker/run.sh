#!/bin/bash

# Run workers for 0MQ

new_workers=3

endpoint1='kernel'
endpoint2='hello'

# IP Address of the router
router_ip='service'
collector_ip='collector'

router_port1=5556
router_port2=5557

collector_port=5558

for ((i=1; i<=$new_workers; i++)) {
	python kernel_generator.py $endpoint1 $i $router_ip $collector_ip \
		$router_port1 &

	python hello_worker.py $endpoint2 $i $router_ip $collector_ip \
		$router_port2 &
}

python kernel_generator.py $endpoint1 $i $router_ip $collector_ip $router_port2
