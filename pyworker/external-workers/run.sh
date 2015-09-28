#!/bin/bash

# Run pyworker for 0MQ
new_workers=7

# IP Address of the router
router_ip='192.168.99.100'
collector_ip='192.168.99.100'
router_port=5556
collector_port=5558


for ((i=1; i<=$new_workers; i++)) {
	python worker.py $i $router_ip $collector_ip $router_port &
}

echo $new_workers ' strated.'
python worker.py $i $router_ip $collector_ip $router_port
