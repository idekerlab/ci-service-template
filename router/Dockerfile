#
# Router and collector for zeromq-based workers
#

FROM continuumio/miniconda3

MAINTAINER Keiichiro Ono <kono@ucsd.edu>

RUN apt-get update && apt-get install -y build-essential
RUN conda update conda
RUN pip install pyzmq

RUN mkdir /router
WORKDIR /router
ADD . /router

EXPOSE 5556 5557 5558

ENTRYPOINT ["/router/run.sh"]