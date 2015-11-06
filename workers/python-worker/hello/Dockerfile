# Docker file for simple Python workers

FROM python:3.5

MAINTAINER Keiichiro Ono <kono@ucsd.edu>

RUN apt-get update && apt-get install -y build-essential
RUN pip install redis pyzmq requests pyaml ciworker==0.2.1

RUN mkdir /workers
WORKDIR /workers
ADD . /workers

EXPOSE 5556 5557 5558

ENTRYPOINT ["/workers/run.sh"]