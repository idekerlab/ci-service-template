# Simple file storage using node.js

FROM node:4.2.2

MAINTAINER Keiichiro Ono <kono@ucsd.edu>

RUN apt-get update && apt-get install -y build-essential

RUN npm update -g && npm install forever node-uuid glob redis -g

RUN mkdir /app
WORKDIR /app
RUN mkdir /app/data
ADD . /app
RUN npm install

EXPOSE 3000

ENTRYPOINT ["/app/run.sh"]