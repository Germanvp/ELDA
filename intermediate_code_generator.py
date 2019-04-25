#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 14:37:32 2019

@author: Juan Manuel Perez & German Villacorta
"""
from semantic_cube import SemanticCube, Operators


class Quadruple:
    """
    Quadruple object definition.
    """

    def __init__(self, op1, op2, operator, result):
        """
        Initializes a new quadruple
        :param op1: The left operand
        :param op2: The right operand
        :param operator: The operator to be applied
        :param result: The operation result
        """
        self.op1 = op1
        self.op2 = op2
        self.operator = operator
        self.result = result

    def __repr__(self):
        return f"\t{self.operator}\t{self.op1}\t{self.op2}\t{self.result}"

    def __str__(self):
        return f"{self.operator},{self.op1},{self.op2},{self.result}"

    def change_result(self, res):
        self.result = res


class ICG:
    """
    Generates intermediate code as a quadruples list
    """

    def __init__(self):
        """
        Initializes the Intermediate Code Generator
        """
        self.quadrupleList = []
        self.stackOperands = []
        self.stackTypes = []
        self.stackOperators = []
        self.stackJumps = []
        self.semantic_cube = SemanticCube()
        self.tempCount = 0  # Para hacer variables nuevas: t1, t2...
        self.paramCount = 0  # Para contar cuantos parametros llevamos. Antes de la llamada.
        self.whenJumps = []
        self.whenOperands = []
        self.whenTypes = []

        self.main_goto_pos = 0

        self.constants = {}

        self.base_global = 5000
        self.base_local = 20000
        self.base_constants = 35000

        self.int_start = 0
        self.float_start = 5000
        self.string_start = 10000
        self.bool_start = 12500

        self.global_counters = [0, 0, 0, 0]
        self.local_counters = [0, 0, 0, 0]
        self.constant_counters = [0, 0, 0, 0]

    def reset_bases(self):
        self.local_counters = [0, 0, 0, 0]

    def get_memory_address(self, memory_type, var_type, value=None):
        """
        Inserta variable en memoria y regresa su direccion para que la puedas
        poner en la tabla de variables.
        """
        # Dependiendo de que tipo sea la variable
        # Type start es donde debe empezar el tipo...
        # Type end es donde debe acabar el tipo...
        if var_type == "int":
            type_start = self.int_start
            type_end = self.float_start - 1
            counter = 0
        elif var_type == "float":
            type_start = self.float_start
            type_end = self.string_start - 1
            counter = 1
        elif var_type == "string":
            type_start = self.string_start
            type_end = self.bool_start - 1
            counter = 2
        elif var_type == "bool":
            type_start = self.bool_start
            type_end = 14999
            counter = 3
        else:
            raise TypeError(f"Unknown type '{var_type}'")

        # Checamos que tipo de memoria es.
        # Y asignamos la direccion: Base + base_de_tipo + sig del tipo
        if memory_type == "global":
            address = self.base_global + type_start + self.global_counters[counter]

            if address > self.base_global + type_end:
                raise TypeError(f"Stack Overflow: Can't fit '{var_type}' into '{memory_type}'")
            self.global_counters[counter] += 1
        elif memory_type == "local":
            address = self.base_local + type_start + self.local_counters[counter]

            if address > self.base_local + type_end:
                raise TypeError(f"Stack Overflow: Can't fit '{var_type}' into '{memory_type}'")
            self.local_counters[counter] += 1
        elif memory_type == "constants":
            if value is None:
                raise TypeError(f"Value must be specified for constants")
            elif value in self.constants.values():
                return [k for k, v in self.constants.items() if v == value].pop()
            address = self.base_constants + type_start + self.constant_counters[counter]

            if address > self.base_constants + type_end:
                raise TypeError(f"Stack Overflow: Can't fit '{var_type}' into '{memory_type}'")
            self.constants[address] = value
            self.constant_counters[counter] += 1
        else:
            raise TypeError(f"Unknown memory '{memory_type}'")

        # if type_start is self.int_start:
        #     self.int_start += 1
        # elif type_start is self.float_start:
        #     self.float_start += 1
        # elif type_start is self.string_start:
        #     self.string_start += 1
        # else:
        #     self.bool_start += 1

        return address

    def generate_quadruple(self):
        """
        Pops both the operators to be applied to the operation and their respective types,
        then generates the temporal variable and adds it to the result if appropriate. If no
        TypeError is risen, the quadruple is generated and added to the list
        """

        # Right y left los puse invertidos, al rato lo cambio.
        # Osea solo los nombres, nos puede causar confusion despues.
        left_operand = self.stackOperands.pop()
        right_operand = self.stackOperands.pop()

        left_type = self.stackTypes.pop()
        right_type = self.stackTypes.pop()

        operator = self.stackOperators.pop()
        operator_enum = Operators(operator)

        result_type = self.semantic_cube.is_valid(right_type, left_type, operator_enum)

        if result_type:
            if operator != "=":

                result = self.get_memory_address("local", result_type)

                # Hacemos el quadruple y lo ponemos en la lista de quadruples.
                # Que rara esta la palabra quadruple despues de que la lees varias veces.
                quadruple = Quadruple(right_operand, left_operand, operator, result)
            else:
                result = left_operand
                quadruple = Quadruple(right_operand, None, operator, result)

            self.quadrupleList.append(quadruple)
            self.stackOperands.append(result)
            self.stackTypes.append(result_type)

    def generate_is_quadruple(self):
        left_operand = self.stackOperands.pop()
        right_operand = self.whenOperands[len(self.whenOperands) - 1]

        left_type = self.stackTypes.pop()
        right_type = self.whenTypes[len(self.whenTypes) - 1]

        operator = self.stackOperators.pop()
        operator_enum = Operators(operator)

        result_type = self.semantic_cube.is_valid(right_type, left_type, operator_enum)

        if result_type:
            result = self.get_memory_address("local", result_type)

            # Hacemos el quadruple y lo ponemos en la lista de quadruples.
            # Que rara esta la palabra quadruple despues de que la lees varias veces.
            quadruple = Quadruple(right_operand, left_operand, operator, result)

            self.quadrupleList.append(quadruple)
            self.stackOperands.append(result)
            self.stackTypes.append(result_type)

    def generate_out_quadruple(self):
        result = self.stackOperands.pop()
        self.stackTypes.pop()

        operator = self.stackOperators.pop()

        quadruple = Quadruple(None, None, operator, result)

        self.quadrupleList.append(quadruple)

    def generate_gotoF(self):
        exp_type = self.stackTypes.pop()
        if exp_type != "bool":
            raise TypeError(f"Conditional expressions must resolve to bool")
        else:
            result = self.stackOperands.pop()
            quadruple = Quadruple(result, None, "GotoF", None)
            self.quadrupleList.append(quadruple)
            self.stackJumps.append(len(self.quadrupleList) - 1)

    def generate_goto(self):
        quadruple = Quadruple(None, None, "Goto", None)
        self.quadrupleList.append(quadruple)

    def generate_main_goto(self):
        quadruple = Quadruple(None, None, "Goto", None)
        self.quadrupleList.append(quadruple)
        self.main_goto_pos = len(self.quadrupleList) - 1

    def generate_else_quadruple(self):
        quadruple = Quadruple(None, None, "Goto", None)
        self.quadrupleList.append(quadruple)
        pos = self.stackJumps.pop()
        self.stackJumps.append(len(self.quadrupleList) - 1)
        self.fill_quadruple(pos)

    def generate_param_quadruple(self, param):
        quadruple = Quadruple(None, None, "param", self.stackOperands.pop())

        self.quadrupleList.append(quadruple)
        self.paramCount = self.paramCount + 1

    def generate_function_call(self, func, return_type):
        # Hacer la nueva variable tN.

        # Si es void entonces no hay necesidad de hacer temporal ni poner
        # un resultado. 
        if return_type != "void":
            result = self.get_memory_address("local", return_type)

            self.stackOperands.append(result)
            self.stackTypes.append(return_type)
        else:
            result = None

        # Generamos el quadruplo, ejemplo t3 = call f 
        # Donde N es el numero de parametros que toma la funcion.
        quadruple = Quadruple(func, self.paramCount, "GOSUB", result)
        self.quadrupleList.append(quadruple)

        # Reiniciamos el contador de parametros.
        self.paramCount = 0

    def fill_goto(self, result):
        pos = len(self.quadrupleList) - 1
        self.quadrupleList[pos].change_result(result)

    def fill_main_goto(self, result):
        self.quadrupleList[self.main_goto_pos].change_result(result)

    def fill_quadruple(self, pos):
        self.quadrupleList[pos].change_result(len(self.quadrupleList) + 1)

    def generate_return_quadruple(self, func_type):
        self.semantic_cube.is_valid(func_type, self.stackTypes.pop(), Operators.RETURN)
        quadruple = Quadruple(self.stackOperands.pop(), None, 'RETURN', None)

        self.quadrupleList.append(quadruple)

    def generate_endproc(self):
        quadruple = Quadruple(None, None, 'ENDPROC', None)
        self.quadrupleList.append(quadruple)

    def generate_era(self, func_name):
        quadruple = Quadruple(func_name, None, 'ERA', None)
        self.quadrupleList.append(quadruple)

    def generate_obj_file(self, name, dir_func):
        with open(f'Testing/{name}_comp.eo', 'w+') as obj_file:
            obj_file.write('## Q ##\n')
            pos = 1
            for i in self.quadrupleList:
                obj_file.write(f"{str(i)}\n")
                pos += 1
            obj_file.write('## DF ##\n')
            obj_file.write(f'{dir_func}\n')
            obj_file.write('## CT ##\n')
            for k, v in self.constants.items():
                obj_file.write(f"{k},{v}\n")
