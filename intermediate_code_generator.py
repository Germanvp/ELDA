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

    def generate_quadruple(self):
        """
        Pops both the operators to be applied to the operation and their respective types,
        then generates the temporal variable and adds it to the result if appropriate. If no
        TypeError is risen, the quadruple is generated and added to the list
        """
        right_operand = self.stackOperands.pop()
        left_operand = self.stackOperands.pop()

        right_type = self.stackTypes.pop()
        left_type = self.stackTypes.pop()

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
                quadruple = Quadruple(left_operand, right_operand, operator, result)
                self.quadrupleList.append(quadruple)
                # print(operator, left_operand, right_operand, result)
            else:
                result = left_operand
                quadruple = Quadruple(right_operand, None, operator, result)
                self.quadrupleList.append(quadruple)
                # print(operator, right_operand, None, result)

            self.stackOperands.append(result)
            self.stackTypes.append(result_type)

    def generate_if_quadruple(self):
        exp_type = self.stackTypes.pop()
        if exp_type != "bool":
            raise TypeError(f"Conditional expressions must resolve to bool")
        else:
            result = self.stackOperands.pop()
            quadruple = Quadruple(result, None, "GotoF", None)
            self.quadrupleList.append(quadruple)
            self.stackJumps.append(len(self.quadrupleList) - 1)

    def generate_else_quadruple(self):
        quadruple = Quadruple(None, None, "Goto", None)
        self.quadrupleList.append(quadruple)
        pos = self.stackJumps.pop()
        self.stackJumps.append(len(self.quadrupleList) - 1)
        self.fill_quadruple(pos)

    def fill_quadruple(self, pos):
        self.quadrupleList[pos].change_result(len(self.quadrupleList))
