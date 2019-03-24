#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 14:37:32 2019

@author: German
"""
from semantic_cube import SemanticCube, Operators
from quadruples import Quadruple

# Intermediate Code Generator
class ICG:
    
    def __init__(self):
        self.quadrupleList = []
        self.stackOperands = []
        self.stackTypes = []
        self.stackOperators = []
        self.semantic_cube = SemanticCube()
        self.tempCount = 0 #Para hacer variables nuevas: t1, t2...
        
    
    def generateQuadruple(self):
        right_operand = self.stackOperands.pop()
        left_operand = self.stackOperands.pop()
        
        right_type = self.stackTypes.pop()
        left_type = self.stackTypes.pop()
        
        
        operator = self.stackOperators.pop()
        operator_enum = Operators(operator)
        
        result_type = self.semantic_cube.is_valid(right_type, left_type, operator_enum)
        
        if(result_type):
            # Hacer la nueva variable tN.
            self.tempCount = self.tempCount + 1
            result = "t" + str(self.tempCount)
            
            # Hacemos el quadruple y lo ponemos en la lista de quadruples.
            # Que rara esta la palabra quadruple despues de que la lees varias veces.
            quadruple = Quadruple(left_operand, right_operand, operator, result)
            self.quadrupleList.append(quadruple)
            
            self.stackOperands.append(result)
            self.stackTypes.append(result_type)
            
            print(operator, left_operand, right_operand, result)

                
        
        
        
        
        
        
        
        
        
        
        
        