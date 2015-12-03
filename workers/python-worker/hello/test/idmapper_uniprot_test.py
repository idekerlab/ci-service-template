# -*- coding: utf-8 -*-
import unittest


from .hello import idmapper

class TestMapper(unittest.TestCase):

    def test_map(self):

        print('\n\n----------  ID Mapper Test Start -------------\n')

        test_query = {
            'ids': ["672", "675"],  # BRCA1 and BRCA2
            'from': "P_ENTREZGENEID",  # From NCBI Entrez Gene ID
            'to': 'GENENAME'  # To human readable gene symbol
        }

        res = idmapper.mapper.convert(
            test_query["ids"], test_query["from"], test_query["to"])

        print(res)
        print('\n----------  ID Mapper Test Finished -------------\n')
