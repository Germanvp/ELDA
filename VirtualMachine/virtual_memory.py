#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 21:11:27 2019

@author: German
"""


class VirtualMemory:

    def __init__(self, parent, size, isMain):
        
        self.isMain = isMain
        
        ### Las direcciones en donde empieza ese espacio en la memoria.
        self.base_global = 5000
        self.base_local = 20000
        self.base_constants = 35000

        ### Dividimos por int, float, strings y bool.
        self.int_start = 0
        self.float_start = 5000
        self.string_start = 10000
        self.bool_start = 12500

        ### Los contadores, para saber en que parte de la memoria va.
        ### Los pondre como un arreglo para que se puedan pasar por referencia
        ### y cambiar el valor de manera mas facil.
        ### en donde el orden es [int, float, string, bool]
        self.counters_global = [0, 0, 0, 0]

        self.counters_local = [0, 0, 0, 0]

        self.counters_constants = [0, 0, 0, 0]
        
        self.counter_execution = 0 if isMain == True else None
        ### La "memoria" osea los arreglos estos fregados.
        self.memory_global = {}
        self.memory_local = {}
        self.memory_constants = {}
        self.memory_execution = {} if isMain == True else None

        ### Para saber donde buscar, por ejemplo las variables globales.
        ### O adentro de dos for loops

        self.parent = parent
        self.size = size
        self.active_record = None
        
        
    def load_obj_file(self, file):
        """
        TODO: What structure will the OBJ file have?
        :param file:
        :return:
        """
        
    def add_scope(self, size):
        if self.isMain:
            new_scope = VirtualMemory(self, size)
    
            if self.counter_execution + size > self.base_execution + 45000:
                raise TypeError(f"Stack Overflow: The execution stack was filled.")
            address = self.base_execution + self.counter_execution
            self.counter_execution = self.counter_execution + size
    
            self.active_record = new_scope
            self.memory_execution[address] = new_scope        

    def insert_into_memory(self, variable, memory_type, var_type):
        """
        Inserta variable en memoria y regresa su direccion para que la puedas
        poner en la tabla de variables.
        """
        ### Dependiendo de que tipo sea la variable
        ### Type start es donde debe empezar el tipo...
        ### Type end es donde debe acabar el tipo...
        if var_type == "int":
            type_start = self.int_start
            type_end = self.float_start - 1
            counter_index = 0
        elif var_type == "float":
            type_start = self.float_start
            type_end = self.string_start - 1
            counter_index = 1

        elif var_type == "string":
            type_start = self.string_start
            type_end = self.bool_start - 1
            counter_index = 2

        elif var_type == "bool":
            type_start = self.bool_start
            type_end = 14999
            counter_index = 3
        else:
            raise TypeError(f"Unknown type '{var_type}'")

        ### Checamos que tipo de memoria es.
        ### Y asignamos la direccion: Base + base_de_tipo + sig del tipo
        if memory_type == "global":
            address = self.base_global + type_start + self.counters_global[counter_index]

            if address > self.base_global + type_end:
                raise TypeError(f"Stack Overflow: Can't fit '{var_type}' into '{memory_type}'")

            self.memory_global[address] = variable
            self.counters_global[counter_index] = self.counters_global[counter_index] + 1
        elif memory_type == "local":
            address = self.base_local + type_start + self.counters_local[counter_index]

            if address > self.base_local + type_end:
                raise TypeError(f"Stack Overflow: Can't fit '{var_type}' into '{memory_type}'")

            self.memory_local[address] = variable
            self.counters_local[counter_index] = self.counters_local[counter_index] + 1
        elif memory_type == "constants":
            address = self.base_constants + type_start + self.counters_constants[counter_index]

            if address > self.base_constants + type_end:
                raise TypeError(f"Stack Overflow: Can't fit '{var_type}' into '{memory_type}'")

            self.memory_constants[address] = variable
            self.counters_constants[counter_index] = self.counters_constants[counter_index] + 1
        else:
            raise TypeError(f"Unknown memory '{memory_type}'")

        return address