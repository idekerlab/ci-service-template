# -*- coding: utf-8 -*-
from ciworker.base_worker import BaseWorker

import logging
import idmapper

logging.basicConfig(level=logging.DEBUG)


class IdMappingWorker(BaseWorker):
    """
    Simple ID mapper using Uniprot API
    """

    def run(self, data):
        logging.info(data)
        logging.info("======== " + str(data["ids"]))
        logging.info("======== " + data["from"])
        logging.info("======== " + data["to"])


        # Convert
        return idmapper.IdMapper.convert(data["ids"], str(data["from"]),
                                         str(data["to"]))
