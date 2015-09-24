# Container for R Workers 
#
FROM bioconductor/release_core

MAINTAINER Keiichiro Ono <kono@ucsd.edu>

# For 0MQ
RUN apt-get update && apt-get install -y libzmq3 libzmq3-dev

# For installing additional R packages
ADD additional_install.R /tmp/
RUN R -f /tmp/additional_install.R

RUN mkdir /workers
WORKDIR /workers
ADD . /workers

EXPOSE 5556 5557 5558 8888

ENTRYPOINT ["/workers/run.sh"]