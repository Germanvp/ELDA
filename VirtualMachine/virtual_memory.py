#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 21:11:27 2019

@author: German y JuanMa.
"""

import json


class VirtualMemory:

    def __init__(self, parent, size):
        # self.isMain = is_main

        # self.counter_execution = 0 if is_main else None

        ### La "memoria" osea los arreglos estos fregados.
        # self.memory_global = {}
        self.memory_local = {}
        # self.memory_constants = {}  ## la necesitamos cuando no sea Main??

        # self.memory_execution = {} if is_main else None

        # self.base_execution = 50000
        self.counter_local = 20000

        ### Para saber donde buscar, por ejemplo las variables globales.
        ### O adentro de dos for loops

        self.parent = parent
        self.size = size
        # self.active_record = None

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


    # def add_scope(self, size):
    #     if self.isMain:
    #         new_scope = VirtualMemory(self, size)
    #
    #         if self.counter_execution + size > self.base_execution + 45000:
    #             raise TypeError(f"Stack Overflow: The execution stack was filled.")
    #
    #         address = self.base_execution + self.counter_execution
    #         self.counter_execution = self.counter_execution + size
    #
    #         self.active_record = new_scope
    #         self.memory_execution[address] = new_scope
    #
    # def insert_into_memory(self, address_variable, address_value):
    #     """
    #     Inserta variable en memoria y regresa su direccion para que la puedas
    #     poner en la tabla de variables.
    #     """
    #     ## TODO: Cala esto esta cnmadre, se pone una palomita y todo.
    #     ### Hay que ver si esto esta bien, estoy 90% seguro que no.
    #
    #     if self.isMain:
    #         self.memory_global[address_variable] = address_value
    #     else:
    #         self.memory_local[address_variable] = address_value
