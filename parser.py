#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 07:10:43 2019

@author: Juan Manuel Perez & German Villacorta
"""

###
#   Parser
###

from ply import yacc
from lexer import tokens


def p_empty(p):
     'empty :'
     pass
 
def p_program(p):
    '''program : declaracion program
               | funcion program
               | main
    '''

def p_main(p):
    '''main : VOID MAIN '(' ')' bloque
    
    '''

def p_bloque(p):
    '''bloque : '{' bloqueD bloqueE return '}'
    
    '''  

def p_return(p):
    '''return : RETURN id
              | RETURN expresion
              | empty
    '''

def p_bloqueD(p):
    '''bloqueD : declaracion bloqueD 
               | empty 
    '''        

def p_bloqueE(p):
    '''bloqueE : estatuto bloqueE
                | empty
    '''

# Checa este. No se si podemos reusar las D' de otros?  
def p_bloque_simp(p):
    '''bloque_simp : '{' bloqueE '}'
    '''
    
def p_declaracion(p):
    '''declaracion : type ID EQUAL expresion ';' 
                    | type ID ';' 
    '''
    
def p_estatuto(p):
    '''estatuto : asignacion
                | condicion
                | in
                | out
                | ciclo
                | llamada
    '''
              
def p_asignacion(p):
    '''asignacion : ID EQUAL expresion ';'
    '''

def p_condicion(p):
    '''condicion : IF '(' expresion ')' bloque_simp
                 | IF '(' expresion ')' bloque_simp ELSE bloque_simp
                 | WHEN ID '{' whencase '}' ';'
    '''
    
def p_whencase(p):
    ''' whencase : IS valor ':' bloque_simp whencase
                 | empty
    '''
    
def p_in(p):
    ''' in : IN '(' ')' ';'
    '''
    
def p_out(p):
    '''out : OUT '(' outD ')' ';'
    '''
    
def p_outD(p):
    '''outD : expresion ',' outD
            | empty
    '''

def p_ciclo(p):
    '''ciclo : FOR ID WITH rango bloque_simp
             | WHILE '(' expresion ')' bloque_simp
    
    '''

def p_rango(p):
    '''rango : RANGE '(' expresion ',' expresion ')'
    '''
    
def p_llamada(p):
    '''llamada : ID '(' llamadaD ')' ';'
    '''

def p_llamadaD(p):
    '''llamadaD : expresion ',' llamadaD
                | empty
    '''
    
def p_expresion(p):
    '''expresion : not expr
                 | not expr AND expresion
                 | not expr OR expresion
    '''

def p_not(p):
    '''not : NOT
           | empty
    '''
    
def p_expr(p):
    '''expr : exp 
            | exp RELOP exp
    '''
def p_exp(p):
    '''exp : termino
           | termino SIMPOPER exp
    '''

def p_termino(p):
    '''termino : factor COMPOPER termino
                | factor
    '''

def p_factor(p):
    '''factor : '(' expresion ')'
              | valor
    '''

def p_valor(p):
    '''valor : llamada
             | id
             | arreglo
             | FALSE
             | TRUE
             | INT
             | FLOAT
             | STRING
    '''

def p_id(p):
    '''id : ID indice
    '''

def p_indice(p):
    '''indice : '[' expresion ']'
              | '[' expresion ']' '[' expresion ']'
              | empty
    '''

def p_arreglo(p):
    '''arreglo : '[' arregloD ']'
    '''

def p_arregloD(p):
    '''arregloD : expresion ',' arregloD
                | empty
    '''

def p_funcion(p): 
    '''funcion : type ID '(' params ')' bloque
                | VOID ID '(' params ')' bloque
    '''

def p_params(p):
    '''params : type ID 
              | type ID ',' params
              | empty
    '''

def p_type(p):
    '''type : TYPE_BOOL
            | TYPE_FLOAT
            | TYPE_INT
            | TYPE_STRING
            | type '[' INT ']'
            | type '[' INT ']' '[' INT ']'
    '''

def p_error(p):
    raise TypeError("Unknown literal '%s'" % (p.value,))

parser = yacc.yacc(start = 'program')

# Por si queremos probar, vamos escribiendo codigo en la terminal.
while True: 
    try: 
        s = input('calc > ')
        parse = parser.parse(s)
        if parse is None:
            print('Correct input')
    except EOFError: 
        break 
