FROM continuumio/miniconda

RUN apt-get update && apt-get install -y g++ make graphviz libgraphviz-dev pkg-config
RUN conda update conda && conda update anaconda
RUN conda install scipy numpy networkx
RUN pip install Flask flask-restful py2cytoscape pygraphviz python-igraph redis rq

RUN mkdir /api
WORKDIR /api

EXPOSE 5000

ENTRYPOINT ["./run.sh"]