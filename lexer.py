#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 07:10:43 2019

@author: Juan Manuel Perez & German Villacorta
"""

from ply import lex
import parser

###
#   Lexer
###

literals = ['(', ')', '{', '}', ',', ':', ';', '.', '[', ']']

#Definimos lista de palabras reservadas
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
            'main': 'MAIN'
        }

tokens = ['INT', 'FLOAT', 'STRING', 'ID', 'EQUAL', 'SIMPOPER', 'COMPOPER', 'RELOP'
          ] + list(reserved.values())

# Los tokens mas sencillos se hacen en una linea
t_SIMPOPER = r'\+|\-'
t_COMPOPER = r'\*|\/'
t_RELOP = r'\<|\>|\<\>|\<\=|\>\=|\=\='
t_EQUAL = r'\='
t_INT = r'\d+'
t_FLOAT = r'([0-9])+\.([0-9])*'
t_STRING = r'"\w*"'
t_ignore_SPACE = r'(\s|\n|\r)+'


def t_ID(t):
    r'[a-zA-Z_]+[a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# t_ignore = " \t"


def t_error(t):
    raise TypeError("Unknown token '%s'" % (t.value[0],))
    t.lexer.skip(1)
    

lexer = lex.lex()

# lex.input('int test = "hola";')
# for token in iter(lex.token, None):
#     print(repr(token.type), repr(token.value))