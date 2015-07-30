#
# Router and collector for zeromq-based Python workers
#

FROM continuumio/miniconda3

MAINTAINER Keiichiro Ono <kono@ucsd.edu>

RUN apt-get update && apt-get install -y build-essential
RUN conda update conda
RUN pip install pyzmq redis Flask flask-restful

RUN mkdir /collector
WORKDIR /collector
ADD . /collector

EXPOSE 5558 6666 5001

ENTRYPOINT ["/collector/run.sh"]