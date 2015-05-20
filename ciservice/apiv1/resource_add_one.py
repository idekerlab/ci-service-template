# -*- coding: utf-8 -*-
from resource_base import MemoryResultResource
from services.add_one import add_one


class AddOneResource(MemoryResultResource):

    def parse_args(self):
        self.parser.add_argument('x', type=int, required=True,
                                 help='An integer X')

    def run_service(self, data):
        return add_one(data)
