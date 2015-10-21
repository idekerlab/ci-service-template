#!/bin/bash

PATH=/usr/lib/jvm/java-8-openjdk-amd64/bin:$PATH

java -version

java -Djava.library.path=/usr/local/lib \
	-jar target/ci-worker-core-0.1.0-jar-with-dependencies.jar \
	-c config.yml