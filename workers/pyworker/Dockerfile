# Docker file for Python workers.
# 
# Designed to run heavy number crunching
#

FROM continuumio/miniconda

MAINTAINER Keiichiro Ono <kono@ucsd.edu>

RUN apt-get update && apt-get install -y build-essential
RUN conda update conda && conda install scipy numpy
RUN pip install Flask redis pyzmq hdsubnetfinder

RUN mkdir /workers
WORKDIR /workers
ADD . /workers

EXPOSE 5556 5557 5558

ENTRYPOINT ["/workers/run.sh"]