"""
Main file for language parsing and semantic processing

Created on Thu Mar 14 17:03:27 2019

@author: Juan Manuel Perez & German Villacorta
"""

import parser
import json

# For parser and lexer testing, writing code on terminal
# int a = 5; int b = 50; int funcA() { int c;} void main(){}

while True:
    try:
        s = input('calc > ')
        parse = parser.parser.parse(s)
        if parse is None:
            print('Correct input')
            print(json.dumps(parser.vars_table.table, indent=2, sort_keys=True))
    except TypeError as ex:
        print(ex)
    except EOFError:
        break
