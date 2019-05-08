#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 14:37:32 2019

@author: Juan Manuel Perez & German Villacorta
"""
from .semantic_cube import SemanticCube, Operators
import json


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
        return f"\t{self.operator}\t{self.op1}\t{self.op2}\t{self.result}\n"

    def __str__(self):
        return f"{self.operator},{self.op1},{self.op2},{self.result}\n"

    def change_result(self, res):
        """
        Changes the quadruple result.
        :param res: The new result to be assigned
        """
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

        self.main_goto_pos = None

        self.constants = {}

        self.base_global = 5000
        self.base_local = 20000
        self.base_constants = 35000

        self.int_start = 0
        self.float_start = 5000
        self.string_start = 10000
        self.bool_start = 12500

        # Counters para saber cuantas variables se han declarado de cada tipo, int, float, string, bool
        self.global_counters = [0, 0, 0, 0]
        self.local_counters = [0, 0, 0, 0]
        self.constant_counters = [0, 0, 0, 0]

    def reset_bases(self):
        """
        Resets local counters
        """
        self.local_counters = [0, 0, 0, 0]

    def get_memory_address(self, memory_type, var_type, size=1, value=None):
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

            if address + size > self.base_global + type_end:
                raise TypeError(f"Stack Overflow: Can't fit '{var_type}' into '{memory_type}'")
            self.global_counters[counter] += size
        elif memory_type == "local":
            address = self.base_local + type_start + self.local_counters[counter]
            if address + size > self.base_local + type_end:
                raise TypeError(f"Stack Overflow: Can't fit '{var_type}' into '{memory_type}'")
            self.local_counters[counter] += size
        elif memory_type == "constants":
            if value is None:
                raise TypeError(f"Value must be specified for constants")
            elif value in self.constants.values():
                return [k for k, v in self.constants.items() if v == value].pop()
            address = self.base_constants + type_start + self.constant_counters[counter]

            if address + size > self.base_constants + type_end:
                raise TypeError(f"Stack Overflow: Can't fit '{var_type}' into '{memory_type}'")
            self.constants[address] = value
            self.constant_counters[counter] += size
        else:
            raise TypeError(f"Unknown memory '{memory_type}'")

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
                self.stackOperands.append(result)
                self.stackTypes.append(result_type)
            else:
                result = left_operand
                quadruple = Quadruple(right_operand, None, operator, result)

            self.quadrupleList.append(quadruple)

    def generate_not_quadruple(self):
        """
        Generates a not quadruple with the next operand in the stack
        """
        operand = self.stackOperands.pop()
        var_type = self.stackTypes.pop()

        operator = self.stackOperators.pop()

        if var_type == 'bool':
            result = self.get_memory_address("local", "bool")

            quadruple = Quadruple(operand, None, operator, result)
            self.quadrupleList.append(quadruple)
            self.stackOperands.append(result)
            self.stackTypes.append('bool')
        else:
            raise TypeError(f"Cannot apply operator 'not' to type '{var_type}'")

    def generate_is_quadruple(self):
        """
        Generates an is quadruple. This is called inside the when declaration in the parser.
        """
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
        """
        Generates an out quadruple when the parser recognizes an out.
        """
        result = self.stackOperands.pop()
        self.stackTypes.pop()

        operator = self.stackOperators.pop()

        quadruple = Quadruple(None, None, operator, result)

        self.quadrupleList.append(quadruple)

    def generate_in_quadruple(self):
        """
        Generates an in quadruple
        """
        result = self.get_memory_address("local", "string")

        operator = self.stackOperators.pop()

        quadruple = Quadruple(None, None, operator, result)

        self.quadrupleList.append(quadruple)
        self.stackOperands.append(result)
        self.stackTypes.append('string')

    def generate_gotoF(self):
        """
        Generates a gotoF with the next operand of the stack as result.
        :return:
        """
        exp_type = self.stackTypes.pop()
        if exp_type != "bool":
            raise TypeError(f"Conditional expressions must resolve to bool")
        else:
            result = self.stackOperands.pop()
            quadruple = Quadruple(result, None, "GotoF", None)
            self.quadrupleList.append(quadruple)
            self.stackJumps.append(len(self.quadrupleList) - 1)

    def generate_goto(self):
        """
        Generates an empty Goto rule.
        """
        quadruple = Quadruple(None, None, "Goto", None)
        self.quadrupleList.append(quadruple)

    def generate_main_goto(self):
        """
        Generates the goto that takes the execution into the main function.
        """
        quadruple = Quadruple(None, None, "Goto", None)
        self.quadrupleList.append(quadruple)
        self.main_goto_pos = len(self.quadrupleList) - 1

    def generate_else_quadruple(self):
        """
        Generates the quadruples needed for the else keyword in a conditional statement.
        """
        quadruple = Quadruple(None, None, "Goto", None)
        self.quadrupleList.append(quadruple)
        pos = self.stackJumps.pop()
        self.stackJumps.append(len(self.quadrupleList) - 1)
        self.fill_quadruple(pos)

    def generate_param_quadruple(self):
        """
        Generates a param quadruple with the next operand in the stack.
        """
        quadruple = Quadruple(None, None, "param", self.stackOperands.pop())

        self.quadrupleList.append(quadruple)
        self.paramCount = self.paramCount + 1

    def generate_function_call(self, func, return_type):
        """
        Generates a GOSUB quadruple.
        :param func: The name of the function to call.
        :param return_type: The return type of the function.
        """
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
        """
        Fills the specified goto with the passed result
        :param result: The value with which to fill the goto
        """
        pos = len(self.quadrupleList) - 1
        self.quadrupleList[pos].change_result(result)

    def fill_main_goto(self, result):
        """
        Fills the main goto with the position of the first quadruple in main
        :param result: The position with which to fill the main goto.
        """
        if self.main_goto_pos is not None:
            self.quadrupleList[self.main_goto_pos].change_result(result)

    def fill_quadruple(self, pos):
        """
        Fills the specified quadruple with the length of the quadrupleList
        :param pos: The position of the quadruple to fill
        """
        self.quadrupleList[pos].change_result(len(self.quadrupleList) + 1)

    def generate_return_quadruple(self, func_type):
        """
        Generates a return quadruple
        :param func_type: The type of the function that is generating the return.
        :return:
        """
        self.semantic_cube.is_valid(func_type, self.stackTypes.pop(), Operators.RETURN)
        quadruple = Quadruple(self.stackOperands.pop(), None, 'RETURN', None)

        self.quadrupleList.append(quadruple)

    def generate_endproc(self):
        """
        Generates an ENDPROC quadruple. Called every time a function finishes.
        """
        quadruple = Quadruple(None, None, 'ENDPROC', None)
        self.quadrupleList.append(quadruple)

    def generate_era(self, func_name):
        """
        Generates the ERA quadruple, which initiates function size in execution memory.
        :param func_name: The function to which ERA will be called
        """
        quadruple = Quadruple(func_name, None, 'ERA', None)
        self.quadrupleList.append(quadruple)

    def generate_analysis_quadruple(self, k_clusters=None):
        """
        Generates all analysis quadruples depending on the next operator.
        :param k_clusters: The amount of clusters with which k_means will be called
        """
        function = self.stackOperators.pop().upper()
        if function in ['MEAN', 'MIN', 'MAX', 'STD', 'VAR', 'MEDIAN', 'SIZE']:
            array_pointer = self.stackOperands.pop()
            # El tipo del arreglo que usaremos para calcular.
            array_type = self.stackTypes.pop()

            if array_type == "string" or array_type == "bool":
                raise TypeError(f"Cannot perform reduce with flexible type")

            result = self.get_memory_address("local", "float")
            self.stackOperands.append(result)
            self.stackTypes.append("float")

            quadruple = Quadruple(array_pointer, None, function, result)
            self.quadrupleList.append(quadruple)
        elif function in ['TYPE']:
            var = self.stackOperands.pop()
            result = self.get_memory_address("local", "string")
            self.stackOperands.append(result)
            self.stackTypes.append("string")

            quadruple = Quadruple(var, None, function, result)
            self.quadrupleList.append(quadruple)
        elif function in ['GRAPH']:
            y = self.stackOperands.pop()
            x = self.stackOperands.pop()

            y_type = self.stackTypes.pop()
            x_type = self.stackTypes.pop()

            plot_type_val = self.stackOperands.pop()
            plot_type_type = self.stackTypes.pop()

            if plot_type_type in ['int', 'float', 'bool']:
                raise TypeError(f"Graph type parameter must be string, not '{plot_type_type}'")

            if y_type in ['string', 'bool'] or x_type in ['string', 'bool']:
                raise TypeError(f"Cannot perform graph with flexible type")

            quadruple = Quadruple(x, y, function, plot_type_val)
            self.quadrupleList.append(quadruple)
        elif function in ['LINEAR_REGRESSION', 'LOGISTIC_REGRESSION']:
            y = self.stackOperands.pop()
            x = self.stackOperands.pop()
            
            # Sacamos los tipos de los arreglos.
            y_type = self.stackTypes.pop()
            x_type = self.stackTypes.pop()

            if y_type in ['string', 'bool'] or x_type in ['string', 'bool']:
                raise TypeError(f"Cannot perform regression with flexible type")
            
            # Las dir de los dos pedazos del arreglo.
            result1 = self.get_memory_address("local", "float")
            result2 = self.get_memory_address("local", "float")
            
            # Para que se pongan en donde se quieren asignar.
            self.stackOperands.append(result1)
            self.stackOperands.append(result2)
            
            self.stackTypes.append("float")
            self.stackTypes.append("float")

            quadruple = Quadruple(x, y, function, result1)
            self.quadrupleList.append(quadruple)
        elif function in ['K_MEANS']:
            x = self.stackOperands.pop()
            k = self.stackOperands.pop()

            # Sacamos los tipos de los arreglos.
            x_type = self.stackTypes.pop()
            k_type = self.stackTypes.pop()

            if x_type in ['string', 'bool']:
                raise TypeError(f"Cannot perform kmeans with flexible type")

            if k_type != 'int':
                raise TypeError("K parameter of kmeans must be int")

            if int(k_clusters) <= 0:
                raise TypeError("K value of kmeans must be positive and greater than 0")

            # Las dir de los dos pedazos del arreglo.
            result1 = self.get_memory_address("local", "float")
            result2 = self.get_memory_address("local", "float")

            # Para que se pongan en donde se quieren asignar.
            self.stackOperands.append(result1)
            self.stackOperands.append(result2)

            self.stackTypes.append("float")
            self.stackTypes.append("float")

            quadruple = Quadruple(x, k, function, result1)
            self.quadrupleList.append(quadruple)
            for i in range(0, int(k_clusters)-1):
                # Las dir de los dos pedazos del arreglo.
                result1 = self.get_memory_address("local", "float")
                result2 = self.get_memory_address("local", "float")

                # Para que se pongan en donde se quieren asignar.
                self.stackOperands.append(result1)
                self.stackOperands.append(result2)

                self.stackTypes.append("float")
                self.stackTypes.append("float")

    def calculate_matrix_index_address(self, base, i, j, dope_vector):
        """
        Generate all quadruples needed for calculating the position of a value in a matrix
        :param base: The base address of the matrix
        :param i: The row in which the desired value is at
        :param j: The column in which the desired value is at
        :param dope_vector: The dope_vector for the array
        """
        columns = self.get_memory_address("constants", "int", value=str(dope_vector[1]))
        rows = self.get_memory_address("constants", "int", value=str(dope_vector[0]))
        zero = self.get_memory_address("constants", "int", value=str(0))
        base = self.get_memory_address("constants", "int", value=str(base))

        # Quads para funcion base + (s1 * d2) + s2
        quadVer1 = Quadruple(j, zero, "VER", rows)
        quadVer2 = Quadruple(i, zero, "VER", columns)

        result_mult = self.get_memory_address("local", "int")
        quadMult = Quadruple(j, columns, "*", result_mult)

        result_add = self.get_memory_address("local", "int")
        quadAdd = Quadruple(result_mult, i, "+", result_add)

        result_address = self.get_memory_address("local", "int")
        quadBaseAdd = Quadruple(base, result_add, "+", result_address)

        self.quadrupleList += [quadVer1, quadVer2, quadMult, quadAdd, quadBaseAdd]

        return result_address

    def calculate_vector_index_address(self, base, i, dope_vector):
        """
        Generate all quadruples needed for calculating the position of a value in a matrix
        :param base: The base address of the matrix
        :param i: The position in which the desired value is at
        :param dope_vector: The dope_vector for the array
        """
        size = self.get_memory_address("constants", "int", value=str(dope_vector[1]))
        zero = self.get_memory_address("constants", "int", value=str(0))
        base = self.get_memory_address("constants", "int", value=str(base))

        # Quads para funcion base + s1
        quadVer = Quadruple(i, zero, "VER", size)

        result_address = self.get_memory_address("local", "int")
        quadSum = Quadruple(i, base, "+", result_address)

        self.quadrupleList += [quadVer, quadSum]

        return result_address

    def create_array_size(self, table):
        """
        Creates the array_size table inside the passed table
        :param table: The table in which the array_sizes table will be
        """
        table["array_sizes"] = {}
        for variable in table["vars"]:
            data = table["vars"][variable]
            if data['is_array']:
                address = data["address"]
                size = data['dope_vector']
                table["array_sizes"][address] = size

    def generate_obj_file(self, name, dir_func):
        """
        Generates the object file based on the quadruple list, the constants table and the function directory
        :param name: The file name that the .eo file will have
        :param dir_func: The function directory
        """
        file = {
            "Quadruples": [(quad.operator, quad.op1, quad.op2, quad.result) for quad in self.quadrupleList],
            "Dir Func": dir_func,
            "Const Table": [(k, v) for k, v in self.constants.items()]
        }

        with open(f'{name[:-5]}.eo', 'w') as obj_file2:
            json.dump(file, obj_file2, separators=(',', ':'))
