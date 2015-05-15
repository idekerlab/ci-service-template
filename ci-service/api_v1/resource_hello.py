# -*- coding: utf-8 -*-
from resource_base import MemoryResultResource
from services.hello import HelloService


class HelloResource(MemoryResultResource):
    """
    Task example: Return posted data after 10 seconds.
    """

    def parse_args(self):
        self.parser.add_argument('name', type=str, required=True, help='Your name')

    def run_service(self, data):
        return HelloService.say_hello(data)
