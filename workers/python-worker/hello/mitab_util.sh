#!/usr/bin/env bash

PSICQUIC_URL="http://www.ebi.ac.uk/Tools/webservices/psicquic/intact/webservices/current/search/interactor/"

FORMAT="format=tab27"

query_url=$PSICQUIC_URL'brca1_human?'$FORMAT

curl -l -s "$query_url" | csvcut -t -c 1,2 | awk -F'[,:]' '{print $2 "\t" $4}'
