FROM bioconductor/release_core

MAINTAINER Keiichiro Ono <kono@ucsd.edu>

RUN apt-get update && apt-get install -y build-essential

RUN apt-get install -y libcurl4-openssl-dev
RUN apt-get install -y libzmq3 libzmq3-dev

# Additional R Packages
ADD additional_install.R /tmp/
RUN R -f /tmp/additional_install.R