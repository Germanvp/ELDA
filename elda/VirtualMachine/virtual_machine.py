#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:45:52 2019

@author: German
"""
import sklearn
from sklearn.linear_model import LinearRegression, LogisticRegression
from .main_memory import MainMemory
import numpy as np
import json
import ast


class VirtualMachine:

    def __init__(self):
        self.main_memory = MainMemory()
        self.array_sizes = {}
        self.procedure_stack = []

    def load_obj_file(self, file_name):
        """
        TODO: What structure will the OBJ file have?
        :param file_name:
        :return:
        """
        file = open(file_name, "r")
        data = json.load(file)

        for const_item in data["Const Table"]:
            address = const_item[0]
            value = const_item[1]
            self.main_memory.memory_constants[address] = self.convert_to_type(value)

        dir_func = ast.literal_eval(data["Dir Func"])

        initial_array_sizes = {}
        initial_array_sizes.update(dir_func["global"]["array_sizes"])
        initial_array_sizes.update(dir_func["main"]["array_sizes"])

        self.procedure_stack.append("main")
        self.array_sizes = initial_array_sizes

        self.process_quadruples(data["Quadruples"], dir_func)

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
            return str(value[1:-1])
        elif '.' in value:
            return float(value)
        try:
            return int(value)
        except ValueError:
            return float(value)

    def process_quadruples(self, quadruple_list, dir_func, ip=0):
        params = []
        return_value = None
        # Para que sepamos de que tamaño son los arreglos.

        while True:
            operator = quadruple_list[ip][0]
            op1 = quadruple_list[ip][1]
            op2 = quadruple_list[ip][2]
            result = quadruple_list[ip][3]
            op1, op2, result = self.process_addresses(op1, op2, result)
            if operator == "+":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                if (isinstance(memory1[op1], str) and not isinstance(memory2[op2], str)) or (
                        isinstance(memory2[op2], str) and not isinstance(memory1[op1], str)):
                    memory_result[result] = str(memory1[op1]) + str(memory2[op2])
                else:
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
                res_type = self.get_type(result)
                memory_result[result] = res_type(memory1[op1])
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

                ## Lo ponemos en el stack de funciones
                ## sacamos los tamaños de sus arreglos si es que tiene.
                # Los tamaños tiene que ser los del global + los de la func.
                self.procedure_stack.append(op1)

                new_array_sizes = {}
                new_array_sizes.update(self.array_sizes)
                new_array_sizes.update(dir_func[op1]["array_sizes"])

                self.array_sizes = new_array_sizes

                #                # Por si queremos checar
                # print(self.procedure_stack, self.array_sizes)

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

                # Quitamos esa funcion del procedure_stack
                # Regresamos a tener los tamaños de los arreglos que teniamos.                
                self.procedure_stack.pop()

                if len(self.procedure_stack) > 0:
                    new_array_sizes = {}
                    new_array_sizes.update(dir_func["global"]["array_sizes"])
                    new_array_sizes.update(dir_func[self.procedure_stack[-1]]["array_sizes"])

                    self.array_sizes = new_array_sizes

                else:
                    self.array_sizes = {}
                #                # Por si queremos checar
                # print(self.procedure_stack, self.array_sizes)

                if return_value is not None:
                    return return_value
                else:
                    break

            elif operator == "VER":
                memory1, memory2, memory_result = self.get_memories(op1, op2, result)
                # Checamos si el numero esta entre el rango de esa dimension.
                if not (memory2[op2] <= memory1[op1] < memory_result[result]):
                    raise TypeError(
                        f"Index {int(memory1[op1])} not in range {int(memory2[op2])}-{int(memory_result[result])}")

                ip += 1
            elif operator == "MEAN":
                memory = self.get_memory(op1)
                memory_result = self.get_memory(result)

                # Sacamos la forma que debe tener el arreglo.
                # Y el arreglo verdad...
                array_shape = self.array_sizes[op1]
                variable = self.construct_dimensional_variable(memory, op1, array_shape)

                memory_result[result] = np.mean(variable)
                ip += 1
            elif operator == "SIZE":
                memory = self.get_memory(op1)
                memory_result = self.get_memory(result)

                # Sacamos la forma que debe tener el arreglo.
                # Y el arreglo verdad...
                array_shape = self.array_sizes[op1]

                memory_result[result] = array_shape[0] * array_shape[1]
                ip += 1
            elif operator == "TYPE":
                memory_result = self.get_memory(result)

                result_value = self.get_type(op1)
                if result_value is int:
                    result_value = "int"
                elif result_value is float:
                    result_value = "float"
                elif result_value is str:
                    result_value = "string"
                else:
                    result_value = "bool"

                memory_result[result] = result_value
                ip += 1
            elif operator == "STD":
                memory = self.get_memory(op1)
                memory_result = self.get_memory(result)

                # Sacamos la forma que debe tener el arreglo.
                # Y el arreglo verdad...
                array_shape = self.array_sizes[op1]
                variable = self.construct_dimensional_variable(memory, op1, array_shape)

                memory_result[result] = np.std(variable)
                ip += 1
            elif operator == "VAR":
                memory = self.get_memory(op1)
                memory_result = self.get_memory(result)

                # Sacamos la forma que debe tener el arreglo.
                # Y el arreglo verdad...
                array_shape = self.array_sizes[op1]
                variable = self.construct_dimensional_variable(memory, op1, array_shape)

                memory_result[result] = np.var(variable)
                ip += 1
            elif operator == "MAX":
                memory = self.get_memory(op1)
                memory_result = self.get_memory(result)

                # Sacamos la forma que debe tener el arreglo.
                # Y el arreglo verdad...
                array_shape = self.array_sizes[op1]
                variable = self.construct_dimensional_variable(memory, op1, array_shape)

                memory_result[result] = np.max(variable)
                ip += 1
            elif operator == "MIN":
                memory = self.get_memory(op1)
                memory_result = self.get_memory(result)

                # Sacamos la forma que debe tener el arreglo.
                # Y el arreglo verdad...
                array_shape = self.array_sizes[op1]
                variable = self.construct_dimensional_variable(memory, op1, array_shape)

                memory_result[result] = np.min(variable)
                ip += 1
            elif operator == "MEDIAN":
                memory = self.get_memory(op1)
                memory_result = self.get_memory(result)

                # Sacamos la forma que debe tener el arreglo.
                # Y el arreglo verdad...
                array_shape = self.array_sizes[op1]
                variable = self.construct_dimensional_variable(memory, op1, array_shape)

                memory_result[result] = np.median(variable)
                ip += 1
            elif operator == "LINEAR_REGRESSION":
                #Sacamos X e Y.
                X_memory = self.get_memory(op1)
                Y_memory = self.get_memory(op2)
                
                X_shape = self.array_sizes[op1]
                Y_shape = self.array_sizes[op2]
                
                # Los arreglos, necesitamos transpuesta para sklearn
                X = self.construct_dimensional_variable(X_memory, op1, X_shape)
                Y = self.construct_dimensional_variable(Y_memory, op2, Y_shape)
                                
                X = (np.array(X)).T
                Y = (np.array(Y)).T
                
                #Memoria en donde se agregaran los parametros.
                params_memory = self.get_memory(result)
                
                clf = LinearRegression().fit(X, Y)
                                
                params_memory[result] = clf.coef_[0][0]
                params_memory[result + 1] = clf.intercept_[0]
                
                ip += 1
            elif operator == "LOGISTIC_REGRESSION":
                #Sacamos X e Y.
                X_memory = self.get_memory(op1)
                Y_memory = self.get_memory(op2)
                
                X_shape = self.array_sizes[op1]
                Y_shape = self.array_sizes[op2]
                
                # Los arreglos, necesitamos transpuesta para sklearn
                X = self.construct_dimensional_variable(X_memory, op1, X_shape)
                Y = self.construct_dimensional_variable(Y_memory, op2, Y_shape)
                                
                X = (np.array(X)).T
                Y = (np.array(Y)).T
                
                #Memoria en donde se agregaran los parametros.
                params_memory = self.get_memory(result)
                
                clf = LogisticRegression().fit(X, Y)
                                
                params_memory[result] = clf.coef_[0][0]
                params_memory[result + 1] = clf.intercept_[0]
                
                ip += 1
             
    def construct_dimensional_variable(self, memory, start, shape):
        """
            Funcion que construye y regresa los vectores y matrices. 
        """
        # Vamos poniendo todos los valores en un arreglo de 1D 
        # en donde el tamaño es la multiplicacion de rows x columns
        variable = []
        size = shape[0] * shape[1]

        # Sacamos y ponemos valores en vector/matriz
        for i in range(0, size):
            variable.append(memory[start + i])

        # Para que sea de la forma que queremos.
        variable = np.reshape(np.array(variable), shape)

        return variable

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

    def get_type(self, address):
        """
        Returns the appropriate type of the value held in the address
        :param address: Address that holds the value
        :return: The type
        """
        if 5000 <= address < 10000 or 20000 <= address < 25000 or 35000 <= address < 40000:
            return int
        elif 10000 <= address < 15000 or 25000 <= address < 30000 or 40000 <= address < 45000:
            return float
        elif 15000 <= address < 17500 or 30000 <= address < 32500 or 45000 <= address < 47500:
            return str
        else:
            return bool
