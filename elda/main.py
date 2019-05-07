"""
Main file for language parsing and semantic processing

Created on Thu Mar 14 17:03:27 2019

@author: Juan Manuel Perez & German Villacorta
"""

import sys
from .Compiler import parser
from .VirtualMachine.virtual_machine import VirtualMachine
import json


def elda():
    args = sys.argv[1:]
    action = args[0]
    assert action in ['-c', '-e'], 'Action must be one of -c (compile) or -e (execute): ' + action

    if action == '-c':
        print('Compiling .elda program...')
        try:
            with open(args[1], 'r') as content_file:
                s = content_file.read()
                if not s:
                    print('Empty file')
                else:
                    parser.parser.parse(s)
                    pos = 1
                    print("    operator\top1\top2\tresult")
                    for i in parser.ic_generator.quadrupleList:
                        print(pos, repr(i))
                        pos += 1
                    for k, v in parser.ic_generator.constants.items():
                        print(k, v)
                    parser.ic_generator.generate_obj_file(args[1], str(parser.vars_table.table))
                    # print(json.dumps(parser.vars_table.table, indent=2, sort_keys=True))
                    # print(json.dumps(parser.vars_table.current_scope, indent=2, sort_keys=True))
                    print(f'Done! Compiled file at {args[1][:-5]}.eo')
        except TypeError as ex:
            print(ex)
        except FileNotFoundError:
            print('File not found')
    elif action == '-e':
        try:
            vm = VirtualMachine()
            vm.load_obj_file(args[1])
        except TypeError as ex:
            print(ex)
        except FileNotFoundError:
            print('Compiled file not found')


if __name__ == '__main__':
    elda()
