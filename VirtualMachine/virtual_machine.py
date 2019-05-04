#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:45:52 2019

@author: German
"""

from VirtualMachine.virtual_memory import VirtualMemory
from VirtualMachine.main_memory import MainMemory
import json
import ast


class VirtualMachine:

    def __init__(self):
        self.main_memory = MainMemory()

    def load_obj_file(self, file_name):
        """
        TODO: What structure will the OBJ file have?
        :param file_name:
        :return:
        """
        file = open(file_name + ".eo", "r")
        data = json.load(file)

        for const_item in data["Const Table"]:
            address = const_item[0]
            value = const_item[1]
            self.main_memory.memory_constants[address] = self.convert_to_type(value)

        self.process_quadruples(data["Quadruples"], ast.literal_eval(data["Dir Func"]))

    @staticmethod
    def convert_to_type(value):
        """

        :param value:
        :return:
        """
        if value is None:
            return None
        if value == 'false' or value == 'true':
            return bool(value)
        elif value[0] == '"' and value[-1] == '"':
            return str(value)
        elif '.' in value:
            return float(value)
        try:
            return int(value)
        except ValueError:
            return float(value)

    def process_quadruples(self, quadruple_list, dir_func, ip=0):
        params = []
        return_value = None
        while True:
            operator = quadruple_list[ip][0]
            op1 = quadruple_list[ip][1]
            op2 = quadruple_list[ip][2]
            result = quadruple_list[ip][3]
            op1, op2, result = self.process_addresses(op1, op2, result)
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
            elif operator == "!=":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                memory_result[result] = memory1[op1] != memory2[op2]
                ip += 1
            elif operator == "and":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                memory_result[result] = memory1[op1] and memory2[op2]
                ip += 1
            elif operator == "or":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                memory_result[result] = memory1[op1] or memory2[op2]
                ip += 1
            elif operator == "not":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                memory_result[result] = not memory1[op1]
                ip += 1
            elif operator == "out":
                memory = self.get_memory(result)
                print(memory[result])
                ip += 1
            elif operator == "in":
                memory = self.get_memory(result)
                memory[result] = input()
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
            elif operator == "ERA":
                function = dir_func[op1]
                parent = self.main_memory.active_record if self.main_memory.active_record is not None else self.main_memory
                self.main_memory.add_scope(parent, function["vars_count"])
                ip += 1
            elif operator == "GOSUB":
                self.main_memory.active_record = self.main_memory.memory_execution[
                    list(self.main_memory.memory_execution.keys())[-1]]

                if int(op2) == dir_func[op1]["params_count"]:
                    if self.main_memory.active_record.check_params(dir_func[op1]["params_type"], params):
                        self.main_memory.active_record.assign_params(params)
                        params.clear()
                        value = self.process_quadruples(quadruple_list, dir_func, dir_func[op1]["func_begin"] - 1)
                        if value is not None:
                            memory = self.get_memory(result)
                            memory[result] = value
                    else:
                        raise TypeError(f"Wrong parameter type at function call for '{op1}'")
                else:
                    raise TypeError(f"Wrong number of parameters for function '{op1}'")
                ip += 1
            elif operator == "RETURN":
                memory = self.get_memory(op1)
                return_value = memory[op1]
                ip += 1
            elif operator == "param":
                memory = self.get_memory(result)
                params.append(memory[result])
                ip += 1
            elif operator == "ENDPROC":
                self.main_memory.remove_scope()
                if return_value is not None:
                    return return_value
                else:
                    break
            elif operator == "VER":
                memory1, memory2, memory_result = self.get_memories(int(op1), int(op2), int(result))
                # Checamos si el numero esta entre el rango de esa dimension.
                if not (int(memory2[op2]) <= int(memory1[op1]) < int(memory_result[result])):
                    raise TypeError(
                        f"Index {int(memory1[op1])} not in range {int(memory2[op2])}-{int(memory_result[result])}")

                ip += 1

    def get_memory(self, address):
        """
        Retrieves the correct memory based on the given address
        :param address: The address of the value
        :return: The correct memory in which to look for the value
        """
        if address is None:
            return None
        if 5000 <= address < 20000:
            return self.main_memory.memory_global
        elif 20000 <= address < 35000:
            return self.main_memory.active_record.memory_local if self.main_memory.active_record is not None else self.main_memory.memory_local
        else:
            return self.main_memory.memory_constants

    def get_memories(self, op1, op2, result):
        """
        Helper for calling the get_memory function over all necessary
        values.
        :param op1: The address for the first operator
        :param op2: The address for the second operator
        :param result: The address for the result
        :return: A list of values
        """
        return self.get_memory(op1), self.get_memory(op2), self.get_memory(result)

    def process_address(self, address):
        """
        Transforms parenthesis addresses into actual value address and returns value
        :param address: The address to be transformed
        :return: The actual address where the value is stored
        """
        if isinstance(address, str) and address[0] == '(':
            address_temp = int(address[1:-1])
            memory = self.get_memory(address_temp)
            return memory[address_temp]
        else:
            return address

    def process_addresses(self, op1, op2, result):
        """
        Helper that applies the process address function to all addresses
        :param op1: The address for the first operator
        :param op2: The address for the second operator
        :param result: The address for the result
        :return: A list of values
        """
        return self.process_address(op1), self.process_address(op2), self.process_address(result)
