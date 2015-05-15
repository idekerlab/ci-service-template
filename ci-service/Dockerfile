#
# Dockerfile for Cytoscape CI service template using Flask
#

FROM continuumio/miniconda

MAINTAINER Keiichiro Ono <kono@ucsd.edu>

RUN apt-get update && apt-get install -y \
		build-essential graphviz libgraphviz-dev \
		pkg-config libxml2-dev
RUN conda update conda && conda install scipy numpy networkx
RUN pip install Flask flask-restful py2cytoscape pygraphviz python-igraph redis rq

RUN mkdir /api
WORKDIR /api
ADD . /api 

EXPOSE 5000

ENTRYPOINT ["/api/run.sh"]