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
        self.paramCount = 0 # Para contar cuantos parametros llevamos. Antes de la llamada.
        self.whenJumps = []
        self.whenOperands = []
        self.whenTypes = []

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
                # Hacer la nueva variable tN.
                self.tempCount = self.tempCount + 1
                result = "t" + str(self.tempCount)

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
            # Hacer la nueva variable tN.
            self.tempCount = self.tempCount + 1
            result = "t" + str(self.tempCount)

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


    def generate_else_quadruple(self):
        quadruple = Quadruple(None, None, "Goto", None)
        self.quadrupleList.append(quadruple)
        pos = self.stackJumps.pop()
        self.stackJumps.append(len(self.quadrupleList) - 1)
        self.fill_quadruple(pos)
        
    def generate_param_quadruple(self, param):
        # Checamos si es un id, string o un solo numero
        # Si no es ninguna de esas es por que es una expresion y tenemos
        # que asignar el ultimo temporal.
        
        if(len(param) == 1 or (param[0] == '"' and param[-1] == '"')):
            quadruple = Quadruple(None, None, "param", param)
        else:
            temp = self.quadrupleList[-1].result
            quadruple = Quadruple(None, None, "param", temp)
            
        self.quadrupleList.append(quadruple)
        self.paramCount = self.paramCount + 1
        
    def generate_function_call(self, func, return_type):       
        # Hacer la nueva variable tN.
        
        # Si es void entonces no hay necesidad de hacer temporal ni poner
        # un resultado. 
        if return_type != "void":
            self.tempCount = self.tempCount + 1
            result = "t" + str(self.tempCount)
            print(result, return_type)

            self.stackOperands.append(result)
            self.stackTypes.append(return_type)
        else:
            result = None
            
        # Generamos el quadruplo, ejemplo t3 = call f 
        # Donde N es el numero de parametros que toma la funcion.
        quadruple = Quadruple(func + "()", self.paramCount, "=", result)
        self.quadrupleList.append(quadruple)
        
        # Reiniciamos el contador de parametros.
        self.paramCount = 0
        
    def fill_goto(self, result):
        pos = len(self.quadrupleList) - 1
        self.quadrupleList[pos].change_result(result)

    def fill_quadruple(self, pos):
        self.quadrupleList[pos].change_result(len(self.quadrupleList) + 1)
