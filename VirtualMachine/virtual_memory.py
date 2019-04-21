#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 21:11:27 2019

@author: German
"""

class VirtualMemory:
    
    def __init__(self, parent, size):
        ### Las direcciones en donde empieza ese espacio en la memoria. 
        ### Base == base en ingles Juanma.
        self.base_global = 5000
        self.base_local = 20000
        self.base_constants = 35000
        
        ### Dividimos por int, float y strings.
        self.int_start = 0
        self.float_start = 5000
        self.string_start = 10000
        self.bool_start = 12500
    
        ### Los contadores, para saber en que parte de la memoria va.
        ### Los pondre como un arreglo para que se puedan pasar por referencia
        ### y cambiar el valor de manera mas facil.
        ### en donde el orden es [int, float, string, bool]
        self.counters_global = [0,0,0,0]

        self.counters_local = [0,0,0,0]

        self.counters_constants = [0,0,0,0]
        
        ### La "memoria" osea los arreglos estos fregados.
        self.memory_global = {}
        self.memory_local = {}
        self.memory_constants = {}
        
        ### Para saber donde buscar, por ejemplo las variables globales.
        ### O adentro de dos for loops
        
        self.parent = parent
        self.size = size
        
            
    def insert_in_memory(self, variable, memory_type, var_type):
        '''
        Inserta variable en memoria y regresa su direccion para que la puedas
        poner en la tabla de variables.
        '''
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
            raise TypeError("Ese tipo lo inventaste o que?")

        ### Checamos que tipo de memoria es.
        ### Y asignamos la direccion: Base + base_de_tipo + sig del tipo
        if memory_type == "global":
            address = self.base_global + type_start + self.counters_global[counter_index]
            
            if address > self.base_global + type_end:
                raise TypeError("StackOverflow o esa madre, ya no se pueden {var_type} en {memory_type")
                
            self.memory_global[address] = variable
            self.counters_global[counter_index] = self.counters_global[counter_index] + 1
        elif memory_type == "local":
            address = self.base_local + type_start + self.counters_local[counter_index]
            
            if address > self.base_local + type_end:
                raise TypeError("StackOverflow o esa madre, ya no se pueden {var_type} en {memory_type")
                          
            self.memory_local[address] = variable
            self.counters_local[counter_index] = self.counters_local[counter_index] + 1
        elif memory_type == "constants":
            address = self.base_constants + type_start + self.counters_constants[counter_index]
            
            if address > self.base_constants + type_end:
                raise TypeError("StackOverflow o esa madre, ya no se pueden {var_type} en {memory_type")
                          
            self.memory_constants[address] = variable
            self.counters_constants[counter_index] = self.counters_constants[counter_index] + 1
        else:
            raise TypeError("Esa memoria que o que? De donde la sacaste?")
            
        return address
    
    def add_scope(self, size):
        newScope = VirtualMemory(self, size)
        
        address = self.base_local + self.counter_local
        
        self.memory_local[address] = newScope
        
        
        
        
        
        
        
        
        
        
        
        
        
        