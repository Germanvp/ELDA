#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser
Created on Fri Mar  8 07:10:43 2019

@author: Juan Manuel Perez & German Villacorta
"""

from ply import yacc
from lexer import tokens
from vars_table import VarsTable
from quadruples import Quadruples, push, pop

vars_table = VarsTable()
quads = Quadruples()


def p_empty(p):
    """empty :"""
    p[0] = None
    pass


def p_program(p):
    """program : declaracion program
               | funcion program
               | main
    """


def p_main_id(p):
    """main_id : void MAIN
    """
    if not vars_table.initialized:
        vars_table.initialize()

    vars_table.create_table(p[2], p[1])


def p_main(p):
    """main : main_id '(' ')' bloque
    """


def p_bloque(p):
    """bloque : '{' bloqueD bloqueE return '}'
    """


def p_return(p):
    """return : RETURN expresion
              | empty
    """


def p_bloqueD(p):
    """bloqueD : declaracion bloqueD
               | empty
    """


def p_bloqueE(p):
    """bloqueE : estatuto bloqueE
                | empty
    """


def p_bloque_simp(p):
    """bloque_simp : '{' bloqueE '}'
    """


# Por si la cago otra vez en cabiarlo, aqui la dejo.
# def p_declaracion_id(p):
#    """declaracion_id : type ID
#    """
#    if not vars_table.initialized:
#        vars_table.initialize()
#
#    if(isinstance(p[1], tuple)):
#        is_array = True
#        dope_vector = (p[1][1])
#        p_type = p[1][0]
#    else:
#        is_array = False
#        dope_vector = None
#        p_type = p[1]
#        
#    vars_table.insert(p[2], p_type, is_array, dope_vector)


def p_declaracion(p):
    """declaracion : type ID EQUAL expresion ';'
                    | type ID ';'
    """
    if not vars_table.initialized:
        vars_table.initialize()

    # Aqui checamos si el tipo es (type[x] || type[x][y] ) o type.
    # Si es un array p[1] debe ser tuple con este formato (temporal) : (type, (rows, columns))
    if isinstance(p[1], tuple):
        is_array = True
        dope_vector = p[1][1]
        p_type = p[1][0]
    else:
        is_array = False
        dope_vector = None
        p_type = p[1]

    # Sacamos el valor que la variable debe tener.
    if len(p) == 6:
        value = p[4]
    else:
        value = None

    vars_table.insert(p[2], p_type, is_array, dope_vector, value)


def p_estatuto(p):
    """estatuto : asignacion
                | condicion
                | in
                | out
                | ciclo
                | llamada
    """


def p_asignacion(p):
    """asignacion : ID EQUAL expresion ';'
    """
    vars_table.update_variable(p[1], p[3])


def p_condicion(p):
    """condicion : IF '(' expresion ')' bloque_simp
                 | IF '(' expresion ')' bloque_simp ELSE bloque_simp
                 | WHEN ID '{' whencase '}' ';'
    """


def p_whencase(p):
    """ whencase : IS valor ':' bloque_simp whencase
                 | empty
    """


def p_in(p):
    """ in : IN '(' ')' ';'
    """


def p_out(p):
    """out : OUT '(' outD ')' ';'
    """


def p_outD(p):
    """outD : expresion ',' outD
            | empty
    """


def p_ciclo(p):
    """ciclo : FOR ID WITH rango bloque_simp
             | WHILE '(' expresion ')' bloque_simp

    """


def p_rango(p):
    """rango : RANGE '(' expresion ',' expresion ')'
    """


def p_llamada(p):
    """llamada : ID '(' llamadaD ')' ';'
    """


def p_llamadaD(p):
    """llamadaD : expresion ',' llamadaD
                | empty
    """


def p_expresion(p):
    """expresion : not expr
                 | not expr and expresion
                 | not expr or expresion
    """
    if len(p) == 3:
        p[0] = p[2]


def p_not(p):
    """not : NOT
           | empty
    """


def p_and(p):
    """and : AND
    """
    push(quads.operator_stack, p[1])


def p_or(p):
    """or : OR
    """
    push(quads.operator_stack, p[1])


def p_simp_oper(p):
    """simp_oper : SIMPOPER
    """
    push(quads.operator_stack, p[1])


def p_comp_oper(p):
    """comp_oper : COMPOPER
    """
    push(quads.operator_stack, p[1])

def p_relop(p):
    """relop : RELOP
    """
    push(quads.operator_stack, p[1])


def p_expr(p):
    """expr : exp
            | exp relop exp
    """
    # Solo regresamos primera expresion, es por mientras.
    p[0] = p[1]


def p_exp(p):
    """exp : termino
           | termino simp_oper exp
    """
    # Solo regresamos primer termino, es por mientras.
    p[0] = p[1]


def p_termino(p):
    """termino : factor comp_oper termino
                | factor
    """
    # Solo regresamos primer factor, es por mientras.
    p[0] = p[1]


def p_factor(p):
    """factor : '(' expresion ')'
              | valor
    """
    # Solo regresamos si es valor, es por mientras.
    if len(p) == 2:
        p[0] = p[1]


def p_valor(p):
    """valor : llamada
             | id
             | arreglo
             | FALSE
             | TRUE
             | INT
             | FLOAT
             | STRING
    """
    # Solo regresamos 1 valor, es por mientras.
    p[0] = p[1]


def p_id(p):
    """id : ID indice
    """


def p_indice(p):
    """indice : '[' expresion ']'
              | '[' expresion ']' '[' expresion ']'
              | empty
    """


def p_arreglo(p):
    """arreglo : '[' arregloD ']'
    """


def p_arregloD(p):
    """arregloD : expresion ',' arregloD
                | empty
    """


def p_funcion_id(p):
    """funcion_id : type ID
                  | void ID
    """
    vars_table.create_table(p[2], p[1])


def p_funcion(p):
    """funcion : funcion_id '(' params ')' bloque
    """


def p_void(p):
    """void : VOID
    """
    p[0] = p[1]


def p_params(p):
    """params : type ID
              | type ID ',' params
              | empty
    """
    # Aqui checamos si el tipo es (type[x] || type[x][y] ) o type.
    # Si es un array p[1] debe ser tuple con este formato (temporal) : (type, (rows, columns))
    if len(p) > 2:
        if isinstance(p[1], tuple):
            is_array = True
            dope_vector = p[1][1]
            p_type = p[1][0]
        else:
            is_array = False
            dope_vector = None
            p_type = p[1]

        vars_table.insert(p[2], p_type, is_array, dope_vector, None)


def p_type(p):
    """type : TYPE_BOOL
            | TYPE_FLOAT
            | TYPE_INT
            | TYPE_STRING
            | type '[' INT ']'
            | type '[' INT ']' '[' INT ']'
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 5:
        p[0] = (p[1], (1, int(p[3])))
    else:
        p[0] = (p[1], (int(p[3]), int(p[6])))


def p_error(p):
    raise TypeError(f"Unknown literal '{p.value}'")


parser = yacc.yacc(start='program')
