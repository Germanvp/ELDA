#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 07:10:43 2019

@author: Juan Manuel Perez & German Villacorta
"""

import ply.lex as lex

###
#   Lexer
###

#Definimos lista de palabras reservadas, (Juanma, reserved es reservado en Ingles)

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
        'func': 'FUNC',
        'return': 'RETURN'
        }

tokens = ['INT', 'FLOAT', 'ID', 'PLUS', 'MINUS', 'GT', 
          'LT', 'SM','LPAREN', 'RPAREN', 'DC', 'LCORCH', 'RCORCH', 'TIMES', 'DIVIDE', 
          'DOTDOT', 'EQUAL', 'COMMA'
          ] + list(reserved.values())

# Los tokens mas sencillos se hacen en una linea
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUAL = r'\='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQRPAREN = r'\['
t_RSQRPAREN = r'\]'
t_SM = r'<>'
t_GT = r'>'
t_LT = r'<'
t_DC = r'\;'
t_LCORCH = r'\{'
t_RCORCH = r'\}'
t_DOTDOT = r'\:'
t_COMMA = r','
t_INT = r'\d+'
t_FLOAT = r'([0-9])+\.([0-9])*'


def t_ID(t):
    r'[a-zA-Z_]+[a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = " \t"

def t_error(t):
    print("Eh caracter ilegal", t.value[0])
    t.lexer.skip(1)
    

lexer = lex.lex()


###
#   Parser
###

def p_empty(p):
     'empty :'
     pass
 
def p_program(p):
    '''program : | programD programF main
    '''
def p_programD(p):
    '''programD : | declaracion programD
                  | empty 
    '''

def p_programF(p):
    '''programF : | funcion programF
                  | empty 
    '''

def p_main(p):
    '''main : | VOID MAIN ( ) bloque
    
    '''
 
### Checar Bloque.  
# Puse que se pudiera no poner declaraciones.   
def p_bloque(p):
    '''bloque : | { bloqueD bloqueE }
    
    '''  

def p_bloqueD(p):
    '''bloqueD : | declaracion bloqueD 
                 | empty 
    '''        

def p_bloqueE(p):
    '''bloqueE : | estatuto bloqueE
                 | empty
    '''

# Checa este. No se si podemos reusar las D' de otros?  
def p_bloque_simp(p):
    '''bloque_simp : | { bloqueE }
    '''
    
def p_declaracion(p):
    '''declaracion : | type ID = expresion ; 
                     | type ID ; 
    '''
    
def p_estatuto(p):
    '''estatuto: | asignacion
                 | condicion
                 | in
                 | out
                 | ciclo
                 | llamada
    '''
              
def p_asignacion(p):
    '''asignacion: | ID = expresion ;
    
    '''

# Checa 
def p_condicion(p):
    '''condicion : | IF ( expresion ) bloque_simp
                   | IF ( expresion ) bloque_simp ELSE bloque_simp
                   | WHEN ID { whencase } ;
    
    '''
    
def p_whencase(p):
    ''' whencase : | IS valor : bloque_simp whencase
                   | empty
    '''
    
def p_in(p):
    ''' in: | IN () ;
    '''
    
def p_out(p):
    '''out: OUT ( outD ) ;
    '''

# Usamos mucho "expresion, " no se si nos conviene hacerlo en
# una regla y ponerlo o dejarlo asi como lo puse. 
    
def p_outD(p):
    '''outD : | expresion, outD
              | expresion
              | empty
    '''

def p_ciclo(p):
    '''ciclo : | FOR ID WITH rango bloque_simp
               | WHILE ( expresion ) bloque_simp
    
    '''

def p_rango(p):
    '''rango : | RANGE ( expresion, expresion )
    '''
    
def p_llamada(p):
    '''llamada : | ID ( llamadaD ) ;
    '''

def p_llamadaD(p):
    '''llamadaD : | expresion, llamadaD
                  | expresion 
                  | empty
    '''
    
def p_expresion(p):
    '''expresion: | expr
                  | NOT expr
                  | expr and expresion
                  | expr or expresion
                  | NOT expr and expresion
                  | NOT expr or expresion
    '''

# Aqui lo cambia para la madre esa que me habias dicho de que se podia:
    # a > b > c y pos que es eso verdad. Que fregados. 
    
def p_expr(p):
    '''expr: | exp 
             | exp <= exp
             | exp >= exp
             | exp > exp
             | exp <> exp
             | exp < exp
             | exp == exp
    '''
def p_exp(p):
    '''exp : | termino
             | termino + exp
             | termino - exp
    '''

def p_termino(p):
    '''termino : | factor
                 | factor * termino
                 | factor / termino
    '''

def p_factor(p):
    '''factor : | ( expresion )
                | valor
    '''

# Aqui no son las palabras reservdas, si no valores de ese tipo.
def p_valor(p):
    '''valor : | llamada
               | id
               | arreglo
               | FALSE
               | TRUE
               | INT
               | FLOAT
               | STRING
    '''
def p_id(p):
    '''id: | ID indice
    '''

def p_indice(p):
    '''indice : | [ expresion ]
                | [ expresion ] [ expresion ]
                | empty
    '''

def p_arreglo(p):
    '''arreglo : | [ arregloD ]
    '''

def p_arregloD(p):
    '''arregloD : | expresion, arregloD
                  | expresion
    '''

def p_funcion(p): 
    '''funcion : | type ID ( params ) bloque
                 | VOID ID ( params ) bloque
    '''

# Para esas funciones que no tienen parametros, se nos fue poner ().
# Estamos mas cerca de ser INTs
def p_params(p):
    '''params : | type ID 
                | type ID, params
                | empty
    '''

# Aqui INT es como si fuera un valor, no la palabra reservada :)
def p_type(p):
    '''type : | BOOL
              | FLOAT
              | INT
              | STRING
              | type [ INT ]
              | type [ INT ] [ INT ]
    '''
# Aqui haces el parser
import ply.yacc as yacc
parser = yacc.yacc(start = 'programa')
    

# Por si queremos probar, vamos escribiendo codigo en la terminal.
while True: 
    try: 
        s = input('calc > ') # Use raw_input on Python 2 
    except EOFError: 
        break 
    
    parser.parse(s)
