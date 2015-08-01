# Simple file storage using node.js

FROM node:latest

MAINTAINER Keiichiro Ono <kono@ucsd.edu>

RUN apt-get update && apt-get install -y build-essential

RUN npm update -g && npm install forever node-uuid redis -g

RUN mkdir /app
WORKDIR /app
ADD . /app
RUN npm install

EXPOSE 3000

ENTRYPOINT ["/app/run.sh"]