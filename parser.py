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
from intermediate_code_generator import ICG

vars_table = VarsTable()
ic_generator = ICG()


def p_empty(p):
    """empty :
    """
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


def p_declaracion(p):
    """declaracion : type ID equal expresion ';'
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

    vars_table.insert(p[2], p_type, is_array, dope_vector)

    ic_generator.stackOperands.append(p[2])
    ic_generator.stackTypes.append(p_type)

    if ic_generator.stackOperators and ic_generator.stackOperators[-1] in ['=']:
        ic_generator.generate_quadruple()


def p_estatuto(p):
    """estatuto : asignacion
                | condicion
                | in
                | out
                | ciclo
                | llamada
    """


def p_equal(p):
    """equal : EQUAL
    """
    ic_generator.stackOperators.append(p[1])


def p_asignacion(p):
    """asignacion : ID equal expresion ';'
                  | ID indice equal expresion ';'
    """
    
    variable = vars_table.search(p[1])

    if variable:
        ic_generator.stackOperands.append(p[1])
        ic_generator.stackTypes.append(variable["type"])
    else:
        raise TypeError(f"'{p[1]}' variable not declared.")
        
    if ic_generator.stackOperators and ic_generator.stackOperators[-1] in ['=']:
        ic_generator.generate_quadruple()


def p_lpar_cond(p):
    """lpar_cond : '('
    """


def p_rpar_cond(p):
    """rpar_cond : ')'
    """
    ic_generator.generate_gotoF()


def p_else(p):
    """else : ELSE
    """
    ic_generator.generate_else_quadruple()


def p_condicion(p):
    """condicion : IF lpar_cond expresion rpar_cond bloque_simp
                 | IF lpar_cond expresion rpar_cond bloque_simp else bloque_simp
                 | WHEN ID '{' whencase '}' ';'
    """
    end = ic_generator.stackJumps.pop()
    ic_generator.fill_quadruple(end)


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
    """outD : expresion
            | expresion ',' outD
            | empty
    """
    ic_generator.stackOperators.append("out")
    ic_generator.generate_out_quadruple()


def p_for(p):
    """for : FOR ID WITH rango
    """
    # Estamos creando nuestro iterador, hasta ahorita solo puede ser int.
    # es el i en for i in range(x,y)
    if not vars_table.initialized:
        vars_table.initialize()
    vars_table.insert(p[2], "int", False, False)

    # Creamos el quadruplo de la asignacion del iterador con valor en el que empieza.
    ic_generator.stackOperands.append(p[2])
    ic_generator.stackTypes.append("int")
    ic_generator.stackOperators.append("=")

    ic_generator.generate_quadruple()

    # Creamos el quadruplo de la suma del iterador mas 1.
    ic_generator.stackOperands.append(p[2])
    ic_generator.stackTypes.append("int")
    ic_generator.stackOperands.append(1)
    ic_generator.stackTypes.append("int")
    ic_generator.stackOperators.append("+")

    ic_generator.generate_quadruple()

    ic_generator.stackJumps.append(len(ic_generator.quadrupleList))

    ic_generator.stackOperands.append(p[2])
    ic_generator.stackTypes.append("int")
    ic_generator.stackOperators.append("=")

    ic_generator.generate_quadruple()

    # Crearemos la condicion para que se detenga. Solo con ints por mientras.
    # ID < N
    ic_generator.stackOperands.append(p[2])
    ic_generator.stackTypes.append("int")
    ic_generator.stackOperators.append("<")
    
    ic_generator.stackTypes.append("int")
    ic_generator.stackOperands.append(p[4])

    ic_generator.generate_quadruple()
        
    # Genera el GotoF. Pues si verdad, que otra cosa puede hacer una funcion 
    # que se llame generate gotoF. 
    ic_generator.generate_gotoF()


def p_while_keyword(p):
    """while_keyword : WHILE
    """
    # Para reconocer el salto correcto en el que se realizan todos los calculos
    # y luego se evalua la condicion.
    ic_generator.stackJumps.append(len(ic_generator.quadrupleList) + 1)


def p_while(p):
    """while : while_keyword '(' expresion ')'
    
    """
    # Saca volumen de cubo.
    ic_generator.generate_gotoF()
    
    
def p_ciclo(p):
    """ciclo : for bloque_simp
             | while bloque_simp

    """
    end = ic_generator.stackJumps.pop()
    revisit = ic_generator.stackJumps.pop()
    
    # LLenamos el goTo que creamos para que vuelva a checar la cond. del loop.
    ic_generator.generate_goto()
    ic_generator.fill_goto(revisit)
    
    # Llenamos el goToF que creamos para cuando no se cumpla la condicion
    # con la linea a la que tiene que saltar.
    ic_generator.fill_quadruple(end)
        
def p_rango(p):
    """rango : RANGE '(' expresion ',' INT ')'
    """
    # Regresamos el valor maximo que puede ser el iterador del if, 
    # esto para usarlo y crear la condicion. Ej. i < 10.
    p[0] = p[5]
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
    p[0] = p[1]


def p_and(p):
    """and : AND
    """
    p[0] = p[1]
    ic_generator.stackOperators.append(p[1])


def p_or(p):
    """or : OR
    """
    p[0] = p[1]
    ic_generator.stackOperators.append(p[1])


def p_simp_oper(p):
    """simp_oper : SIMPOPER
    """
    p[0] = p[1]
    # 3. 
    ic_generator.stackOperators.append(p[1])


def p_comp_oper(p):
    """comp_oper : COMPOPER
    """
    p[0] = p[1]
    # 2.
    ic_generator.stackOperators.append(p[1])


def p_relop(p):
    """relop : RELOP
    """
    p[0] = p[1]
    # #?.
    ic_generator.stackOperators.append(p[1])


def p_lpar(p):
    """lpar : '('
    """
    p[0] = p[1]
    ic_generator.stackOperators.append(p[1])


def p_rpar(p):
    """rpar : ')'
    """
    p[0] = p[1]
    ic_generator.stackOperators.pop()


def p_expr(p):
    """expr : exp
            | exp relop exp
    """
    # Solo regresamos primera expresion, es por mientras.
    p[0] = p[1]

    if ic_generator.stackOperators and ic_generator.stackOperators[-1] in ['or', 'and']:
        ic_generator.generate_quadruple()


def p_exp(p):
    """exp : termino
           | termino simp_oper exp
    """
    # Solo regresamos primer termino, es por mientras.
    p[0] = p[1]

    # ? No sale en ppt.
    if ic_generator.stackOperators and ic_generator.stackOperators[-1] in ['>', '<', '<>', '==', '<=', '>=']:
        ic_generator.generate_quadruple()


def p_termino(p):
    """termino : factor comp_oper termino
                | factor
    """
    # Solo regresamos primer factor, es por mientras.
    p[0] = p[1]

    # 4.
    if ic_generator.stackOperators and ic_generator.stackOperators[-1] in ['+', '-']:
        ic_generator.generate_quadruple()


def p_factor(p):
    """factor : lpar expresion rpar
              | valor
    """
    # Solo regresamos si es valor, es por mientras.
    if len(p) == 2:
        p[0] = p[1]

    # 5.
    if ic_generator.stackOperators and ic_generator.stackOperators[-1] in ['*', '/']:
        ic_generator.generate_quadruple()


def p_constant_i(p):
    """constant_i : INT
    """
    p[0] = p[1]
    ic_generator.stackOperands.append(p[1])
    ic_generator.stackTypes.append("int")


def p_constant_f(p):
    """constant_f : FLOAT
    """
    p[0] = p[1]
    ic_generator.stackOperands.append(p[1])
    ic_generator.stackTypes.append("float")


def p_constant_b(p):
    """constant_b : TRUE
                  | FALSE
    """
    p[0] = p[1]
    ic_generator.stackOperands.append(p[1])
    ic_generator.stackTypes.append("bool")


def p_constant_s(p):
    """constant_s : STRING
    """
    p[0] = p[1]
    ic_generator.stackOperands.append(p[1])
    ic_generator.stackTypes.append("string")


def p_valor(p):
    """valor : llamada
             | id
             | arreglo
             | constant_b
             | constant_i
             | constant_f
             | constant_s
    """
    # Solo regresamos 1 valor, es por mientras.
    p[0] = p[1]


def p_id(p):
    """id : ID indice
    """
    # Checamos si el id existe. Lo ponemos en stacks.

    # 1.
    variable = vars_table.search(p[1])

    if variable:
        ic_generator.stackOperands.append(p[1])
        ic_generator.stackTypes.append(variable["type"])
    else:
        raise TypeError(f"'{p[1]}' variable not declared.")


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

        vars_table.insert(p[2], p_type, is_array, dope_vector)


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
