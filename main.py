"""
Main file for language parsing and semantic processing

Created on Thu Mar 14 17:03:27 2019

@author: Juan Manuel Perez & German Villacorta
"""

import parser

# For parser and lexer testing, writing code on terminal
while True:
    try:
        s = input('calc > ')
        parse = parser.parser.parse(s)
        if parse is None:
            print('Correct input')
            print(parser.function_directory)
    except TypeError as ex:
        print(ex)
    except EOFError:
        break
