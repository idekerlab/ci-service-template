# -*- coding: utf-8 -*-

import requests

import logging

logging.basicConfig(level=logging.DEBUG)


UNIPROT_API_ID_MAPPER_URL = 'http://www.uniprot.org/mapping'


class IdMapper():
    """Simple ID Mapping service.
    This class simply wrap Uniprot API and generate the result in JSON
    instead of TSV.
    """

    @staticmethod
    def convert(id_list, type_from, type_to):

        # convert list of IDs into a space-delimited string
        ids = ' '.join(id_list)

        payload = {
            'from': type_from,
            'to': type_to,
            'format': 'tab',
            'query': ids
        }

        res = requests.get(UNIPROT_API_ID_MAPPER_URL, params=payload)
        tsv_result = res.text
        lines = tsv_result.split("\n")

        logging.info(lines)

        # Prepare result as a dictionary
        result = {}

        for line in lines:
            if line.startswith("From"):
                continue
            if line == "":
                continue

            pair = line.split("\t")
            if len(pair) != 2:
                continue

            key = pair[0]
            values = []
            if key in result:
                values = result[key]

            values.append(pair[1])

            result[key] = values

        return result
