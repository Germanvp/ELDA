#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 21:11:27 2019

@author: German y JuanMa.
"""


class VirtualMemory:

    def __init__(self, parent, size):
        self.memory_local = {}

        self.counter_local = 20000

        self.parent = parent
        self.size = size

    def assign_params(self, params):
        """
        Assigns all parameters to a local address in memory
        :param args: The list of parameter values
        """
        for param in params[::-1]:
            self.memory_local[self.counter_local] = param
            self.counter_local += 1

    def check_params(self, types, params):
        zipped = zip(types[::-1], params)
        for t, p in zipped:
            if t == 'i' and type(p) is not int:
                return False
            elif t == 'f' and type(p) is not float:
                return False
            elif t == 'b' and type(p) is not bool:
                return False
            elif t == 's' and type(p) is not str:
                return False
        return True
