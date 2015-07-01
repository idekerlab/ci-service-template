#!/bin/bash

# Run workers for 0MQ
new_workers=5

# IP Address of the router
router_ip='10.0.1.17'
router_port=5557

for ((i=1; i<=$new_workers; i++)) {
	python worker.py $router_ip $router_port &
}

echo $new_workers ' strated.'

/bin/bash