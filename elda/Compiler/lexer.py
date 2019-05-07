#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lexer
Created on Fri Mar  8 07:10:43 2019

@author: Juan Manuel Perez & German Villacorta
"""

from ply import lex

literals = ['(', ')', '{', '}', ',', ':', ';', '.', '[', ']']

reserved = {
            'if': 'IF',
            'else': 'ELSE',
            'when': 'WHEN',
            'with': 'WITH',
            'range': 'RANGE',
            'true': 'TRUE',
            'false': 'FALSE',
            'in': 'IN',
            'out': 'OUT',
            'for': 'FOR',
            'is': 'IS',
            'while': 'WHILE',
            'and': 'AND',
            'or': 'OR',
            'not': 'NOT',
            'return': 'RETURN',
            'int': 'TYPE_INT',
            'bool': 'TYPE_BOOL',
            'float': 'TYPE_FLOAT',
            'string': 'TYPE_STRING',
            'void': 'VOID',
            'main': 'MAIN',
            'mean': 'MEAN',
            'std': 'STD',
            'var': 'VAR',
            'min': 'MIN',
            'max': 'MAX',
            'size': 'SIZE',
            'type': 'TYPE',
            'graph': 'GRAPH',
            'median': 'MEDIAN',
        }

tokens = ['INT', 'FLOAT', 'STRING', 'ID', 'EQUAL', 'COMPOPER', 'RELOP', 'SUM', 'MINUS'
          ] + list(reserved.values())

t_SUM = r'\+'
t_MINUS = r'\-'
t_COMPOPER = r'\*|\/'
t_RELOP = r'\!\=|\<\=|\>\=|\=\=|\<|\>'
t_EQUAL = r'\='
t_INT = r'\d+'
t_FLOAT = r'([0-9])+\.([0-9])*'
t_STRING = r'".*"' #r'"[a-zA-Z0-9_\s]*"'
t_ignore_SPACE = r'(\s|\n|\r)+'


def t_ID(t):
    r'[a-zA-Z_]+[a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise TypeError(f"Unknown token '{t.value[0]}'")
    t.lexer.skip(1)
    

lexer = lex.lex()

# lex.input('int test = "hola";')
# for token in iter(lex.token, None):
#     print(repr(token.type), repr(token.value))