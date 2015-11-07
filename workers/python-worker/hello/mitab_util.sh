#!/usr/bin/env bash

# Sample shell script to call external service and
#

PSICQUIC_URL="http://www.ebi.ac.uk/Tools/webservices/psicquic/intact/webservices/current/search/interactor/"
FORMAT="format=tab27"

# Compile a REST API call
query_url=$PSICQUIC_URL$1'?'$FORMAT

# execute and process the result.
curl -l -s "$query_url" | csvcut -t -c 1,2 | awk -F'[,:]' '{print $2 " " $4}'
