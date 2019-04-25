#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 21:11:27 2019

@author: German y JuanMa pa que no llore.
"""

import json


class VirtualMemory:

    def __init__(self, parent, size, isMain):
        
        self.isMain = isMain

        self.counter_execution = 0 if isMain else None
        
        ### La "memoria" osea los arreglos estos fregados.
        self.memory_global = {}
        self.memory_local = {}
        self.memory_constants = {} ## la necesitamos cuando no sea Main??
        
        self.memory_execution = {} if isMain else None

        ### Para saber donde buscar, por ejemplo las variables globales.
        ### O adentro de dos for loops

        self.parent = parent
        self.size = size
        self.active_record = None
        

        
    def add_scope(self, size):
        if self.isMain:
            new_scope = VirtualMemory(self, size)
    
            if self.counter_execution + size > self.base_execution + 45000:
                raise TypeError(f"Stack Overflow: The execution stack was filled.")
                
            address = self.base_execution + self.counter_execution
            self.counter_execution = self.counter_execution + size
    
            self.active_record = new_scope
            self.memory_execution[address] = new_scope
            
        
    def insert_into_memory(self, address_variable, address_value):
        """
        Inserta variable en memoria y regresa su direccion para que la puedas
        poner en la tabla de variables.
        """
        ## TODO: Cala esto esta cnmadre, se pone una palomita y todo.
        ### Hay que ver si esto esta bien, estoy 90% seguro que no.
        
        if self.isMain:
            self.memory_global[address_variable] = address_value
        else:
            self.memory_local[address_variable] = address_value
    
    
    
