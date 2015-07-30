#!/bin/bash

# Run workers for 0MQ
new_workers=2

# IP Address of the router
router_ip='service'
collector_ip='collector'
router_port=5556
collector_port=5558

cat /etc/hosts

for ((i=1; i<=$new_workers; i++)) {
	python worker.py $i $router_ip $collector_ip $router_port &
}

echo $new_workers ' strated.'
python worker.py $i $router_ip $collector_ip $router_port
