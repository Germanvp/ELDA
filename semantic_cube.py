#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 10:57:45 2019

@author: Juan Manuel Perez & German Villacorta
"""
from enum import Enum


class Operators(Enum):
    """
    Enumeration that defines the string values for all operators
    """

    SUM = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    DIVISION = "/"
    GRT_THAN = ">"
    LWR_THAN = "<"
    GRT_EQ_THAN = ">="
    LWR_EQ_THAN = "<="
    EQUAL = "=="
    AND = "and"
    OR = "or"
    ASSIGN = "="
    OUT = "out"
    RETURN = "return"
    DIFF = "!="


class SemanticCube:
    """
    Handles all calls to the semantic cube.
    """

    def __init__(self):
        """
        Initializes the semantic cube.
        """
        self.semantic_cube = {
            'int': {
                'int': {
                    Operators.SUM: 'int',
                    Operators.SUBTRACTION: 'int',
                    Operators.MULTIPLICATION: 'int',
                    Operators.DIVISION: 'float',
                    Operators.GRT_THAN: 'bool',
                    Operators.LWR_THAN: 'bool',
                    Operators.GRT_EQ_THAN: 'bool',
                    Operators.LWR_EQ_THAN: 'bool',
                    Operators.EQUAL: 'bool',
                    Operators.DIFF: 'bool',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'int',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'int'
                },
                'float': {
                    Operators.SUM: 'float',
                    Operators.SUBTRACTION: 'float',
                    Operators.MULTIPLICATION: 'float',
                    Operators.DIVISION: 'float',
                    Operators.GRT_THAN: 'bool',
                    Operators.LWR_THAN: 'bool',
                    Operators.GRT_EQ_THAN: 'bool',
                    Operators.LWR_EQ_THAN: 'bool',
                    Operators.EQUAL: 'bool',
                    Operators.DIFF: 'bool',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'Ret_Error'
                },
                'bool': {
                    Operators.SUM: 'Error',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.GRT_EQ_THAN: 'Error',
                    Operators.LWR_EQ_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.DIFF: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'Ret_Error'
                },
                'string': {
                    Operators.SUM: 'string',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.GRT_EQ_THAN: 'Error',
                    Operators.LWR_EQ_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.DIFF: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'Ret_Error'
                }
            },
            'float': {
                'int': {
                    Operators.SUM: 'float',
                    Operators.SUBTRACTION: 'float',
                    Operators.MULTIPLICATION: 'float',
                    Operators.DIVISION: 'float',
                    Operators.GRT_THAN: 'bool',
                    Operators.LWR_THAN: 'bool',
                    Operators.GRT_EQ_THAN: 'bool',
                    Operators.LWR_EQ_THAN: 'bool',
                    Operators.EQUAL: 'bool',
                    Operators.DIFF: 'bool',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'Ret_Error'
                },
                'float': {
                    Operators.SUM: 'float',
                    Operators.SUBTRACTION: 'float',
                    Operators.MULTIPLICATION: 'float',
                    Operators.DIVISION: 'float',
                    Operators.GRT_THAN: 'bool',
                    Operators.LWR_THAN: 'bool',
                    Operators.GRT_EQ_THAN: 'bool',
                    Operators.LWR_EQ_THAN: 'bool',
                    Operators.EQUAL: 'bool',
                    Operators.DIFF: 'bool',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'float',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'float'
                },
                'bool': {
                    Operators.SUM: 'Error',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.GRT_EQ_THAN: 'Error',
                    Operators.LWR_EQ_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.DIFF: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'Ret_Error'
                },
                'string': {
                    Operators.SUM: 'string',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.GRT_EQ_THAN: 'Error',
                    Operators.LWR_EQ_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.DIFF: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'Ret_Error'
                }
            },
            'bool': {
                'int': {
                    Operators.SUM: 'Error',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.GRT_EQ_THAN: 'Error',
                    Operators.LWR_EQ_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.DIFF: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'Ret_Error'
                },
                'float': {
                    Operators.SUM: 'Error',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.GRT_EQ_THAN: 'Error',
                    Operators.LWR_EQ_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.DIFF: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'Ret_Error'
                },
                'bool': {
                    Operators.SUM: 'Error',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.GRT_EQ_THAN: 'Error',
                    Operators.LWR_EQ_THAN: 'Error',
                    Operators.EQUAL: 'bool',
                    Operators.DIFF: 'bool',
                    Operators.AND: 'bool',
                    Operators.OR: 'bool',
                    Operators.ASSIGN: 'bool',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'bool'
                },
                'string': {
                    Operators.SUM: 'Error',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.GRT_EQ_THAN: 'Error',
                    Operators.LWR_EQ_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.DIFF: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'Ret_Error'
                }
            },
            'string': {
                'int': {
                    Operators.SUM: 'string',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.GRT_EQ_THAN: 'Error',
                    Operators.LWR_EQ_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.DIFF: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'Ret_Error'
                },
                'float': {
                    Operators.SUM: 'string',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.GRT_EQ_THAN: 'Error',
                    Operators.LWR_EQ_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.DIFF: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'Ret_Error'
                },
                'bool': {
                    Operators.SUM: 'Error',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.GRT_EQ_THAN: 'Error',
                    Operators.LWR_EQ_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.DIFF: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'Ret_Error'
                },
                'string': {
                    Operators.SUM: 'string',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.GRT_EQ_THAN: 'Error',
                    Operators.LWR_EQ_THAN: 'Error',
                    Operators.EQUAL: 'bool',
                    Operators.DIFF: 'bool',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'string',
                    Operators.OUT: 'Error',
                    Operators.RETURN: 'string'
                }
            }
        }

    def is_valid(self, left_type, right_type, operator):
        """
        Determines if a combination of types is valid based on the semantic cube.
        :param left_type: Left type of the operation
        :param right_type: Right type of the operation
        :param operator: Operator being applied to the types
        :return: Result type if valid, raises TypeError otherwise
        """
        
        if 'Error' not in self.semantic_cube[left_type][right_type][operator]:
            return self.semantic_cube[left_type][right_type][operator]
        if self.semantic_cube[left_type][right_type][operator] == 'Ret_Error':
            raise TypeError(f"Type mismatch: Cannot return type '{right_type}' from function of type '{left_type}'")
        raise TypeError(
            f"Type mismatch: Cannot apply operator '{repr(operator)}' to types '{left_type}' and '{right_type}'")

