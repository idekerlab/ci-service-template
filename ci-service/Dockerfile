FROM continuumio/miniconda

RUN apt-get update && apt-get install -y \
		g++ build-essential graphviz libgraphviz-dev pkg-config libxml2-dev
RUN conda update conda
RUN conda install scipy numpy networkx
RUN pip install Flask flask-restful py2cytoscape pygraphviz python-igraph redis rq

RUN mkdir /api
WORKDIR /api
ADD . /api

EXPOSE 5000

ENTRYPOINT ["/api/run.sh"]