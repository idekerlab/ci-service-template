# -*- coding: utf-8 -*-


class IdGenerator():

    def __init__(self):
        self.__counter = 1

    def next_id(self):
        self.__counter += 1
        return self.__counter
