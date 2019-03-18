#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 20:53:40 2019

@author: Juan Manuel Perez & German Villacorta
"""


class VarsTable:

    def __init__(self):
        self.table = None
        self.current_type = None
        self.current_scope = None
        self.initialized = False

    def initialize(self):
        """
        Table es la tabla de variables
        Parent es un apuntador a su padre
        Current type es el tipo actual de la var/func que estamos declarando.
        Nuestro current scope, es como un pointer. En python las variables
        son referencias a objetos.

        Entradas de tabla deben ser [id] = {type, is_array, dope_vector}
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

    # Funcion que inserta una variable a la tabla.
    def insert(self, var_id, var_type, is_array, dope_vector, value):
        
        if var_id not in self.current_scope["vars"] and var_id not in self.table["global"]["vars"]:
            table_entry = {
                "type": var_type,
                "is_array": is_array,
                "dope_vector": dope_vector,
                "value": value
            }

            self.current_scope["vars"][var_id] = table_entry
        else:
            raise TypeError("Variable already declared '%s" % (var_id))


    # Funcion que updetea una variable en la tabla. Sirve para asignaciones.
    def update_variable(self, var_id, value):
        
        if var_id in self.current_scope["vars"]:
            self.current_scope["vars"][var_id]["value"] = value
        elif var_id in self.table["global"]["vars"]:
            self.table["global"]["vars"][var_id]["value"] = value
            
        else:
            raise TypeError("Variable not declared '%s" % (var_id))  
            

    ### Crea una nueva tabla. Duh. Parent es un apuntador a la tabla que la creo.
    def create_table(self, table_id, return_type):
        if table_id not in self.table:
            new_table = {
                "type": return_type,
                "vars": {}
            }

            self.table[table_id] = new_table
            self.current_scope = self.table[table_id]
        else:
            raise TypeError("Function already declared '%s'" % (table_id))

    # Busca en la tabla en la que esta o en las tablas que la contienen.
    # Usa un aux para no tener que pasar self.current_scope en ply.

    def search(self, var_id):
        return self.search_aux(var_id, self.current_scope)

    # Namas busca recursivamente si esta en tabla actual, si no se va a la de
    # "arriba" hasta toparse con pared o encontrarla.

    def search_aux(self, var_id, scope):
        if scope is None:
            return 0

        if var_id in scope["vars"]:
            return scope["vars"][var_id]

        return self.search_aux(var_id, self.table["global"])

##Imprimir bonito.
#        
# import json
# vars_table = VarsTable()
# vars_table.initialize()
# vars_table.insert("a","int", 0, None)
#
# vars_table.create_table("main", "void")
# vars_table.insert("b", "string", 1, (10, 100))
#
# vars_table.create_table("input", "string")
# vars_table.insert("c", "string", 0, None)
#
# vars_table.current_scope
#
# vars_table.search("a")
##print(json.dumps(vars_table.table, indent=8, sort_keys=True))