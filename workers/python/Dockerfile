# Docker file for Python workers.
# 
# Designed to run heavy number crunching
#

FROM continuumio/miniconda

MAINTAINER Keiichiro Ono <kono@ucsd.edu>

RUN apt-get update && apt-get install -y \
		build-essential graphviz libgraphviz-dev \
		pkg-config libxml2-dev
RUN conda update conda && conda install scipy numpy networkx
RUN pip install py2cytoscape pygraphviz python-igraph pyzmq

RUN mkdir /workers
WORKDIR /workers
ADD . /workers

EXPOSE 5557 5558

ENTRYPOINT ["/workers/run.sh"]