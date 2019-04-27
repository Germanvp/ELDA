#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:45:52 2019

@author: German
"""

from VirtualMachine.virtual_memory import VirtualMemory
import json


class VirtualMachine:
    
    def __init__(self):
        self.active_memory = VirtualMemory(None, 10, True)
        
        
    
    def load_obj_file(self, file_name):
        """
        TODO: What structure will the OBJ file have?
        :param file:
        :return:
        """
        file = open(file_name + ".eo", "r")
        data = json.load(file)
        
        
        for const_item in data["Const Table"]:
            address = const_item[0]
            value = const_item[1]
            self.active_memory.memory_constants[address] = value
            
        
        self.process_quadruples(data["Quadruples"], data["Dir Func"])
    
    def process_quadruples(self, quadrupleList, dir_func):
        for operator, op1, op2, result in quadrupleList:
            if operator == "+":
                print(".")
            elif operator == "-":
                print(".")
            elif operator == "*":
                print(".")
            elif operator == "/":
                print(".")
            elif operator == "=":
                self.active_memory.insert_into_memory(op1, result)
            elif operator == "GOSUB":
                print(".")
            elif operator == "ENDPROC":
                print(".")

    
    
    
    
    