#!/bin/bash

new_workers=3

router_ip='service'
collector_ip='collector'

hello_port=5559

echo "Starting service..."

for ((i=1; i<=$new_workers; i++)) {
	python hello_worker.py "hello" $i $router_ip $collector_ip \
		$hello_port &
}

python hello_worker.py "hello" $i $router_ip $collector_ip \
		$hello_port
