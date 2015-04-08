# Cytoscape CI Service Template

## What is this?
This is a toy example to setup services in Docker containers.

## Requirments
You need to install the following to try this sample:

* Git
* Docker
* Docker Compose

## Services
This template include following containers:

* Redis for task queue
* Actual services deployed as Flask-based RESTful API

## Quick Start

1. Make sure you have Docker installed on your workstation.
1. [Install docker-compose](http://docs.docker.com/compose/)
1. Clone this repository
1. ```cd ci-service-template```
1. ```docker-compose build```
1. ```docker-compose up```
1. (For Mac/Windows) Check _boot2docker_'s IP address
1. Open the top-level service URL: ```http://192.168.59.103/v1```
1. If you can see the following, the services are running:

```json
{
	"serviceName": "Cytoscape CI template service",
	"version": "0.1.0"
}
```

For more information, read this wiki:

* [CI Wiki](https://github.com/idekerlab/ci-service-template/wiki)

## Questions?
Send me an email (kono ucsd edu).