#
# Monitor and collector for zeromq-based Python workers
#
FROM python:3.4

MAINTAINER Keiichiro Ono <kono@ucsd.edu>

RUN apt-get update && apt-get install -y build-essential
RUN pip install pyzmq redis

RUN mkdir /collector
WORKDIR /collector
ADD . /collector

EXPOSE 5558 6666 5001

ENTRYPOINT ["/collector/run.sh"]