#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 20:53:40 2019

@author: Juan Manuel Perez & German Villacorta
"""


class VarsTable:
    """
    Class that manages creation and insertion of functions and variables into
    the variable table and function directory.
    """

    def __init__(self):
        self.table = None
        self.current_type = None
        self.current_scope = None
        self.initialized = False

    def initialize(self):
        """
        Initializes the variable table with the global function and sets the
        global function as the current scope.
        """
        self.table = {
            "global": {
                "type": "void",
                "vars": {}
            }
        }

        self.current_type = ""
        self.current_scope = self.table["global"]
        self.initialized = True

    def insert(self, var_id, var_type, is_array, dope_vector, address):
        """
        Inserts a new variable of type var_type to the current scope. Raises TypeError
        if the variable was already declared.
        :param var_id: The variable name to be inserted.
        :param var_type: The variable type.
        :param is_array: If the variable is an array declaration.
        :param dope_vector: If it is an array, the dope vector states when it starts and when it ends in memory.
        """
        if var_id not in self.current_scope["vars"] and var_id not in self.table["global"]["vars"]:
            table_entry = {
                "type": var_type,
                "is_array": is_array,
                "dope_vector": dope_vector,
                "address": address
            }

            self.current_scope["vars"][var_id] = table_entry

        else:
            raise TypeError(f"Variable already declared '{var_id}'")

    def create_table(self, table_id, return_type):
        """
        Creates a new table for a function. Raises TypeError if the function is already
        declared
        :param table_id: The name of the function to be created.
        :param return_type: The return type expected from the function.
        """
        if table_id not in self.table:
            new_table = {
                "type": return_type,
                "vars": {},
                "params_type": "",
                "params_count": 0,
                "vars_count": 0,
                "func_begin": None
            }

            self.table[table_id] = new_table
            self.current_scope = self.table[table_id]
        else:
            raise TypeError("Function already declared '%s'" % table_id)

    def search(self, var_id):
        """
        Searches for the variable in the current scope and the parent.
        :param var_id: The name of the id to be searched.
        :return: The variable if found.
        """
        return self.search_aux(var_id, self.current_scope)

    def search_aux(self, var_id, scope):
        """
        Recursively searches for the variable in the given scope, if not found, searches
        for it in the global function.
        :param var_id: The name of the variable to search for.
        :param scope: The scope to search in.
        :return: The variable if found, False otherwise.
        """
        if scope is None:
            return 0
        if var_id in scope["vars"]:
            return scope["vars"][var_id]
        elif var_id in self.table["global"]["vars"]:
            return self.table["global"]["vars"][var_id]
        raise TypeError(f"Variable {var_id} not declared")
