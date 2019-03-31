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
    EQUAL = "=="
    AND = "and"
    OR = "or"
    ASSIGN = "="
    OUT = "out"


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
                    Operators.EQUAL: 'bool',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'int',
                    Operators.OUT: 'Error'
                },
                'float': {
                    Operators.SUM: 'float',
                    Operators.SUBTRACTION: 'float',
                    Operators.MULTIPLICATION: 'float',
                    Operators.DIVISION: 'float',
                    Operators.GRT_THAN: 'bool',
                    Operators.LWR_THAN: 'bool',
                    Operators.EQUAL: 'bool',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error'
                },
                'bool': {
                    Operators.SUM: 'Error',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error'
                },
                'string': {
                    Operators.SUM: 'string',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error'
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
                    Operators.EQUAL: 'bool',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error'
                },
                'float': {
                    Operators.SUM: 'float',
                    Operators.SUBTRACTION: 'float',
                    Operators.MULTIPLICATION: 'float',
                    Operators.DIVISION: 'float',
                    Operators.GRT_THAN: 'bool',
                    Operators.LWR_THAN: 'bool',
                    Operators.EQUAL: 'bool',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'float',
                    Operators.OUT: 'Error'
                },
                'bool': {
                    Operators.SUM: 'Error',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error'
                },
                'string': {
                    Operators.SUM: 'string',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error'
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
                    Operators.EQUAL: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error'
                },
                'float': {
                    Operators.SUM: 'Error',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error'
                },
                'bool': {
                    Operators.SUM: 'Error',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.EQUAL: 'bool',
                    Operators.AND: 'bool',
                    Operators.OR: 'bool',
                    Operators.ASSIGN: 'bool',
                    Operators.OUT: 'Error'
                },
                'string': {
                    Operators.SUM: 'Error',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error'
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
                    Operators.EQUAL: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error'
                },
                'float': {
                    Operators.SUM: 'string',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error'
                },
                'bool': {
                    Operators.SUM: 'Error',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.EQUAL: 'Error',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'Error',
                    Operators.OUT: 'Error'
                },
                'string': {
                    Operators.SUM: 'string',
                    Operators.SUBTRACTION: 'Error',
                    Operators.MULTIPLICATION: 'Error',
                    Operators.DIVISION: 'Error',
                    Operators.GRT_THAN: 'Error',
                    Operators.LWR_THAN: 'Error',
                    Operators.EQUAL: 'bool',
                    Operators.AND: 'Error',
                    Operators.OR: 'Error',
                    Operators.ASSIGN: 'string',
                    Operators.OUT: 'Error'
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
        
        if self.semantic_cube[left_type][right_type][operator] is not 'Error':
            return self.semantic_cube[left_type][right_type][operator]
        raise TypeError(
            f"Type mismatch: Cannot apply operator '{repr(operator)}' to types '{left_type}' and '{right_type}'")

