"""
Main file for language parsing and semantic processing

Created on Thu Mar 14 17:03:27 2019

@author: Juan Manuel Perez & German Villacorta
"""

import parser

# For parser and lexer testing, writing code on terminal
# int a = 5; int b = 50; int funcA() { int c;} void main(){}
# int a = 5; string b = "a"; int funcA(string c) { int d;} void main(){int[4] ar;}
# int a = 5; void main(){ int b = 0; a = 7; b = 100;}
# int a = 5; int b = 50; int funcA(int test, int test2) { int c;} void main(){}

# Quadruples Tests
# int a = 1; int b = 2; int c = 3; void main() { int d = a + b * c;}
# int a = 1; int b = 2; int c = 3; void main() { int d = (a + b) * (c + b);}

while True:
    try:
        s = input('calc > ')
        parse = parser.parser.parse(s)
        if parse is None:
            print('Correct input')
            # print(json.dumps(parser.vars_table.table, indent=2, sort_keys=True))
    except TypeError as ex:
        print(ex)
    except EOFError:
        break
