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

    def process_quadruples(self, quadruple_list, dir_func):
        ip = 0
        # for operator, op1, op2, result in quadruple_list:
        while True:
            operator = quadruple_list[ip][0]
            op1 = quadruple_list[ip][1]
            op2 = quadruple_list[ip][2]
            result = quadruple_list[ip][3]
            if operator == "+":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                memory_result[result] = memory1[op1] + memory2[op2]
                ip += 1
            elif operator == "-":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                memory_result[result] = memory1[op1] - memory2[op2]
                ip += 1
            elif operator == "*":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                memory_result[result] = memory1[op1] * memory2[op2]
                ip += 1
            elif operator == "/":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                memory_result[result] = memory1[op1] / memory2[op2]
                ip += 1
            elif operator == "=":
                # self.active_memory.insert_into_memory(op1, result)
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                memory_result[result] = memory1[op1]
                ip += 1
            elif operator == ">":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                memory_result[result] = memory1[op1] > memory2[op2]
                ip += 1
            elif operator == "<":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                memory_result[result] = memory1[op1] < memory2[op2]
                ip += 1
            elif operator == ">=":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                memory_result[result] = memory1[op1] >= memory2[op2]
                ip += 1
            elif operator == "<=":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                memory_result[result] = memory1[op1] <= memory2[op2]
                ip += 1
            elif operator == "==":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                memory_result[result] = memory1[op1] <= memory2[op2]
                ip += 1
            elif operator == "<>":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                memory_result[result] = memory1[op1] != memory2[op2]
                ip += 1
            elif operator == "out":
                memory = self.get_memory(result)
                print(memory[result])
                ip += 1
            elif operator == "GotoF":
                memory = self.get_memory(op1)
                if not memory[op1]:
                    ip = int(result) - 1
                else:
                    ip += 1
            elif operator == "GotoV":
                memory = self.get_memory(op1)
                if memory[op1]:
                    ip = int(result) - 1
                else:
                    ip += 1
            elif operator == "Goto":
                ip = int(result) - 1
            elif operator == "GOSUB":
                print(".")
                ip += 1
            elif operator == "ENDPROC":
                break

    def get_memory(self, address):
        """
        Retrieves the correct memory based on the given address
        :param address:
        :return:
        """
        if address is None:
            return None
        if 5000 <= address < 20000:
            return self.active_memory.memory_global if self.active_memory.parent is None else self.active_memory.parent.memory_global
        elif 20000 <= address < 35000:
            return self.active_memory.memory_local
        else:
            return self.active_memory.memory_constants

    def get_memories(self, op1, op2, result):
        """

        :param op1:
        :param op2:
        :param result:
        :return:
        """
        return self.get_memory(op1), self.get_memory(op2), self.get_memory(result)
