"""
Main file for language parsing and semantic processing

Created on Thu Mar 14 17:03:27 2019

@author: Juan Manuel Perez & German Villacorta
"""

import parser
import json
from VirtualMachine.virtual_machine import VirtualMachine

# For parser and lexer testing, writing code on terminal
# int a = 5; int b = 50; int funcA() { int c;} void main(){}
# int a = 5; string b = "a"; int funcA(string c) { int d;} void main(){int[4] ar;}
# int a = 5; void main(){ int b = 0; a = 7; b = 100;}
# int a = 5; int b = 50; int funcA(int test, int test2) { int c;} void main(){}

# Quadruples Tests
# int a = 1; int b = 2; int c = 3; void main() { int d = a + b * c;}
# int a = 1; int b = 2; int c = 3; void main() { int d = (a + b) * (c + b);}

try:
    name = input('File name: ')
    with open("Testing/" + name + ".elda", 'r') as content_file:
        s = content_file.read()
        if not s:
            print('Empty file')
        else:
            result = parser.parser.parse(s)
            # if result is None:
            #     print('File parsed correctly!')
            #     pos = 1
            #     print("    operator\top1\top2\tresult")
            #     for i in parser.ic_generator.quadrupleList:
            #         print(pos, repr(i))
            #         pos += 1
            #     for k, v in parser.ic_generator.constants.items():
            #         print(k, v)

            parser.ic_generator.generate_obj_file(name, str(parser.vars_table.table))
#            print(json.dumps(parser.vars_table.table, indent=2, sort_keys=True))
#            print(json.dumps(parser.vars_table.current_scope, indent=2, sort_keys=True))

            ### TEST
            vm = VirtualMachine()
            vm.load_obj_file("Testing/" + name + "_comp")

except TypeError as ex:
    # print(json.dumps(parser.vars_table.table, indent=2, sort_keys=True))
    # pos = 1
    # print("    operator\top1\top2\tresult")
    # for i in parser.ic_generator.quadrupleList:
    #     print(pos, repr(i))
    #     pos += 1
    # for k, v in parser.ic_generator.constants.items():
    #     print(k, v)
    print(ex)
except FileNotFoundError as ex:
    print(ex)
    print(f"File not found")
