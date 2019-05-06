#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser
Created on Fri Mar  8 07:10:43 2019

@author: Juan Manuel Perez & German Villacorta
"""

from ply import yacc
from .vars_table import VarsTable
from .intermediate_code_generator import ICG
from .lexer import tokens

vars_table = VarsTable()
ic_generator = ICG()


def p_empty(p):
    """empty :
    """
    p[0] = None
    pass


# def p_program(p):
#     """program : declaracion program
#                | funcion program
#                | main
#     """

def p_program(p):
    """program : program_d
    """
    ic_generator.fill_main_goto(vars_table.table["main"]["func_begin"])


def p_program_d(p):
    """program_d : declaracion program_d
                 | program_f
    """


def p_program_f(p):
    """program_f : funcion program_f
                 | program_m
    """


def p_program_m(p):
    """program_m : main
    """


def p_main_id(p):
    """main_id : void MAIN
    """
    if not vars_table.initialized:
        vars_table.initialize()

    ic_generator.reset_bases()
    # vars_table.current_scope["vars_count"] = len(vars_table.current_scope["vars"])
    if vars_table.current_scope is not vars_table.table["global"]:
        ic_generator.create_array_size(vars_table.current_scope)
        del vars_table.current_scope["vars"]

    vars_table.create_table(p[2], p[1])


def p_main(p):
    """main : main_id '(' r_main_par bloque_void
    """
    ic_generator.reset_bases()
    vars_table.current_scope["vars_count"] = len(vars_table.current_scope["vars"])
    
    # Guardamos tamaños de arreglos para usarlos en VM.
    ic_generator.create_array_size(vars_table.current_scope)
    del vars_table.current_scope["vars"]
    
    # Guardamos tamaños de arreglos para usarlos en VM.
    ic_generator.create_array_size(vars_table.table["global"])
    del vars_table.table["global"]["vars"]



def p_r_main_par(p):
    """r_main_par : ')'
    """
    vars_table.current_scope["func_begin"] = len(ic_generator.quadrupleList) + 1


def p_bloque_void(p):
    """bloque_void : '{' bloqueD bloqueE '}'
    """
    ic_generator.generate_endproc()


def p_bloque_return(p):
    """bloque_return : '{' bloqueD bloqueE return '}'
    """
    ic_generator.generate_endproc()


def p_return(p):
    """return : RETURN expresion ';'
    """
    ic_generator.generate_return_quadruple(vars_table.current_scope["type"])


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
        size = dope_vector[0] * dope_vector[1]
    else:
        is_array = False
        dope_vector = None
        p_type = p[1]
        size = 1

    if vars_table.current_scope is vars_table.table["global"]:
        address = ic_generator.get_memory_address("global", p_type, size)
    else:
        address = ic_generator.get_memory_address("local", p_type, size)

    vars_table.insert(p[2], p_type, is_array, dope_vector, address)

    # Si es un vector/matriz tenemos que asignar el valor a cada posicion.
    if dope_vector:
        # Checamos si ya existe una asignacion para el vector/matriz.
        if ic_generator.stackOperators and ic_generator.stackOperators[-1] in ['=']:
            ic_generator.stackOperators.pop()
            # Vamos poniendo de ultimo al primero. 
            # Yo se, esta feo asi el for loop.
            for i in range(size - 1, -1, -1):
                ic_generator.stackOperators.append("=")
                ic_generator.stackOperands.append(address + i)

                ic_generator.stackTypes.append(p_type)
                ic_generator.generate_quadruple()
        else:
            # Tenemos que inicializarlo como quiera.
            if p_type == "string":
                init_value = ""
            elif p_type == "int":
                init_value = 0
            elif p_type == "float":
                init_value = 0.0
            elif p_type == "bool":
                init_value = False

            init_value = ic_generator.get_memory_address("constants", p_type, value=str(init_value))

            # Vamos poniendo de ultimo al primero. 
            # Para que el otro no se sienta solo.
            for i in range(size - 1, -1, -1):
                ic_generator.stackOperands.append(init_value)
                ic_generator.stackOperators.append("=")
                ic_generator.stackOperands.append(address + i)

                ic_generator.stackTypes.append(p_type)
                ic_generator.stackTypes.append(p_type)
                ic_generator.generate_quadruple()
    else:
        if ic_generator.stackOperators and ic_generator.stackOperators[-1] in ['=']:
            ic_generator.stackOperands.append(address)
            ic_generator.stackTypes.append(p_type)
            ic_generator.generate_quadruple()


def p_estatuto(p):
    """estatuto : asignacion
                | condicion
                | when
                | in ';'
                | out
                | ciclo_w
                | ciclo_f
                | llamada ';'
    """


def p_equal(p):
    """equal : EQUAL
    """
    ic_generator.stackOperators.append(p[1])


def p_asignacion(p):
    """asignacion : id equal expresion ';'
    """
    # Con los arreglos p[1] ahora regresa (id, offset)
    # si no es un arreglo el offset es 0.
    variable = vars_table.search(p[1][0])
    if variable:
        address = f"({p[1][1]})" if (variable["is_array"]) else variable["address"]
        ic_generator.stackOperands.append(address)
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


def p_when_id(p):
    """when_id : ID
    """
    variable = vars_table.search(p[1])

    if variable:
        ic_generator.whenOperands.append(variable["address"])
        ic_generator.whenTypes.append(variable["type"])
    else:
        raise TypeError(f"'{p[1]}' variable not declared.")


def p_when(p):
    """when : WHEN when_id '{' whencase '}'
    """
    for i in ic_generator.whenJumps:
        ic_generator.quadrupleList[i].change_result(len(ic_generator.quadrupleList) + 1)
    ic_generator.fill_quadruple(ic_generator.stackJumps.pop())
    ic_generator.whenJumps.clear()
    ic_generator.whenOperands.pop()
    ic_generator.whenTypes.pop()


def p_when_is(p):
    """when_is : IS valor
    """
    if len(ic_generator.whenJumps) > 0:
        ic_generator.fill_quadruple(ic_generator.stackJumps.pop())
    ic_generator.stackOperators.append("==")
    ic_generator.generate_is_quadruple()
    ic_generator.generate_gotoF()


def p_case(p):
    """case : when_is bloque_simp
    """
    ic_generator.generate_goto()
    ic_generator.whenJumps.append(len(ic_generator.quadrupleList) - 1)


def p_whencase(p):
    """whencase : case whencase
                 | empty
    """


def p_condicion(p):
    """condicion : IF lpar_cond expresion rpar_cond bloque_simp
                 | IF lpar_cond expresion rpar_cond bloque_simp else bloque_simp
    """
    end = ic_generator.stackJumps.pop()
    ic_generator.fill_quadruple(end)


def p_in(p):
    """ in : IN '(' ')'
    """
    ic_generator.stackOperators.append("in")
    ic_generator.generate_in_quadruple()


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
    # es el i en for i with range(x,y)
    if not vars_table.initialized:
        vars_table.initialize()

    address = ic_generator.get_memory_address("local", "int")
    vars_table.insert(p[2], "int", False, False, address)

    temp = ic_generator.stackOperands[-1]
    temp_type = ic_generator.stackTypes[-1]
    ic_generator.stackOperands.pop()
    ic_generator.stackTypes.pop()

    # Creamos el quadruplo de la asignacion del iterador con valor en el que empieza.
    ic_generator.stackOperands.append(address)
    ic_generator.stackTypes.append("int")
    ic_generator.stackOperators.append("=")

    ic_generator.generate_quadruple()

    # Crearemos la condicion para que se detenga. Solo con ints por mientras.
    # ID < N
    ic_generator.stackOperands.append(address)
    ic_generator.stackTypes.append("int")
    ic_generator.stackOperators.append("<")

    ic_generator.stackOperands.append(temp)
    ic_generator.stackTypes.append(temp_type)

    ic_generator.generate_quadruple()

    ic_generator.stackJumps.append(len(ic_generator.quadrupleList))

    # Genera el GotoF. Pues si verdad, que otra cosa puede hacer una funcion 
    # que se llame generate gotoF. 
    ic_generator.generate_gotoF()
    p[0] = p[2]


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


def p_ciclo_w(p):
    """ciclo_w : while bloque_simp

    """
    end = ic_generator.stackJumps.pop()
    revisit = ic_generator.stackJumps.pop()

    # LLenamos el goTo que creamos para que vuelva a checar la cond. del loop.
    ic_generator.generate_goto()
    ic_generator.fill_goto(revisit)

    # Llenamos el goToF que creamos para cuando no se cumpla la condicion
    # con la linea a la que tiene que saltar.
    ic_generator.fill_quadruple(end)


def p_ciclo_f(p):
    """ciclo_f : for bloque_simp
    """
    variable = vars_table.current_scope["vars"][p[1]]
    if variable is not None:
        address = variable["address"]
    else:
        raise TypeError(f"Variable {p[1]} not declared")
    # Creamos el quadruplo de la suma del iterador mas 1.
    ic_generator.stackOperands.append(address)
    ic_generator.stackTypes.append("int")

    const_address = ic_generator.get_memory_address("constants", "int", 1, '1')

    ic_generator.stackOperands.append(const_address)
    ic_generator.stackTypes.append("int")
    ic_generator.stackOperators.append("+")

    ic_generator.generate_quadruple()

    ic_generator.stackOperands.append(address)
    ic_generator.stackTypes.append("int")
    ic_generator.stackOperators.append("=")

    ic_generator.generate_quadruple()

    end = ic_generator.stackJumps.pop()
    revisit = ic_generator.stackJumps.pop()

    # LLenamos el goTo que creamos para que vuelva a checar la cond. del loop.
    ic_generator.generate_goto()
    ic_generator.fill_goto(revisit)

    # Llenamos el goToF que creamos para cuando no se cumpla la condicion
    # con la linea a la que tiene que saltar.
    ic_generator.fill_quadruple(end)


def p_rango(p):
    """rango : RANGE '(' expresion ',' expresion ')'
    """
    # Regresamos el valor maximo que puede ser el iterador del if, 
    # esto para usarlo y crear la condicion. Ej. i < 10.
    p[0] = p[5]


def p_llamada(p):
    """llamada : llamada_id lpar llamadaD rpar
    """
    if not vars_table.initialized:
        vars_table.initialize()

    if p[1] in vars_table.table:
        # Que tipo regresa la funcion.
        return_type = vars_table.table[p[1]]["type"]

        ic_generator.generate_function_call(p[1], return_type)
    else:
        raise TypeError(f"'{p[1]}' function not declared.")

    p[0] = ic_generator.quadrupleList[-1].result


def p_llamada_id(p):
    """llamada_id : ID
    """
    ic_generator.generate_era(p[1])

    p[0] = p[1]


# Expresion para que se puedan guardar los parametros como parametros, duh.
def p_expresionL(p):
    """expresionL : expresion
    
    """
    ic_generator.generate_param_quadruple(p[1])


def p_llamadaD(p):
    """llamadaD : expresionL ',' llamadaD
                | expresionL
                | empty
    """

# Para funciones como mean, std, var etc..
def p_llamada_analisis(p):
    """llamada_analisis : analisis_id '(' ID ')'
    
    """
    variable = vars_table.search(p[3])
    
    ## Checamos si la variable existe y si es un arreglo.
    if variable:
        if variable["is_array"]:
            address = variable["address"]
            ic_generator.stackOperands.append(address)
            ic_generator.stackTypes.append(variable["type"])
            
            ic_generator.generate_analysis_quadruple()
        else:
            raise TypeError(f"Parameter for function '{p[1]}' must be an array")
        
    
def p_analisis_id(p):
    """analisis_id : MEAN
                   | STD
                   | VAR
                   | MIN
                   | MAX
                   | MEDIAN
    
    """
    p[0] = p[1]
    ic_generator.stackOperators.append(p[1])
    
    
def p_expresion(p):
    """expresion : not expr
                 | not expr and expresion
                 | not expr or expresion
    """
    if len(p) == 3:
        p[0] = p[2]

    if ic_generator.stackOperators and ic_generator.stackOperators[-1] in ['not']:
        ic_generator.generate_not_quadruple()


def p_not(p):
    """not : NOT
           | empty
    """
    p[0] = p[1]
    if p[1] is not None:
        ic_generator.stackOperators.append(p[1])


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
    """simp_oper : SUM
                 | MINUS
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
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1:]

    if ic_generator.stackOperators and ic_generator.stackOperators[-1] in ['or', 'and']:
        ic_generator.generate_quadruple()


def p_exp(p):
    """exp : termino
           | termino simp_oper exp
    """
    # Solo regresamos primer termino, es por mientras.
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1:]

    # ? No sale en ppt.
    if ic_generator.stackOperators and ic_generator.stackOperators[-1] in ['>', '<', '!=', '==', '<=', '>=']:
        ic_generator.generate_quadruple()


def p_termino(p):
    """termino : factor comp_oper termino
               | factor
    """
    # Solo regresamos primer factor, es por mientras.
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1:]

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
    else:
        p[0] = p[1]

    # 5.
    if ic_generator.stackOperators and ic_generator.stackOperators[-1] in ['*', '/']:
        ic_generator.generate_quadruple()


def p_minus(p):
    """minus : MINUS
             | empty
    """
    p[0] = p[1]


def p_constant_i(p):
    """constant_i : minus INT
    """
    if p[1] == '-':
        p[0] = f'-{p[2]}'
        address = ic_generator.get_memory_address("constants", "int", 1, f'-{p[2]}')
    else:
        p[0] = p[2]
        address = ic_generator.get_memory_address("constants", "int", 1, p[2])
    ic_generator.stackOperands.append(address)
    ic_generator.stackTypes.append("int")


def p_constant_f(p):
    """constant_f : minus FLOAT
    """
    if p[1] == '-':
        p[0] = f'-{p[2]}'
        address = ic_generator.get_memory_address("constants", "float", 1, f'-{p[2]}')
    else:
        p[0] = p[2]
        address = ic_generator.get_memory_address("constants", "float", 1, p[2])
    ic_generator.stackOperands.append(address)
    ic_generator.stackTypes.append("float")


def p_constant_b(p):
    """constant_b : TRUE
                  | FALSE
    """
    p[0] = p[1]
    address = ic_generator.get_memory_address("constants", "bool", 1, p[1])
    ic_generator.stackOperands.append(address)
    ic_generator.stackTypes.append("bool")


def p_constant_s(p):
    """constant_s : STRING
    """
    p[0] = p[1]
    address = ic_generator.get_memory_address("constants", "string", 1, p[1])
    ic_generator.stackOperands.append(address)
    ic_generator.stackTypes.append("string")


def p_valor(p):
    """valor : llamada
             | llamada_analisis
             | id
             | arreglo
             | in
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
        if variable["is_array"]:
            if p[2] is None:
                raise TypeError(f"Array values must be followed by an index, at array call for '{p[1]}'")
            # Aqui sacamos las filas y las columas del dope vector
            # indices [i][j] y calculamos la direccion. Regresamos tupla por si
            # es asignacion.
            base = variable["address"]
            dope_vector = variable["dope_vector"]

            i = ic_generator.stackOperands.pop()
            ic_generator.stackTypes.pop()

            # Si es un vector o matriz.
            if dope_vector[0] == 1:
                j = 1
                address = ic_generator.calculate_vector_index_address(base, i, dope_vector, p[1])
            else:
                j = ic_generator.stackOperands.pop()
                ic_generator.stackTypes.pop()
                address = ic_generator.calculate_matrix_index_address(base, i, j, dope_vector, p[1])

            ic_generator.stackOperands.append(f"({address})")
            ic_generator.stackTypes.append(variable["type"])

            # Regresamos el offset tambien, para que cuando busque la dir en
            # la tabla de variables no se ponga la base si no base + address
            p[0] = p[1], address
        else:
            ic_generator.stackOperands.append(variable["address"])
            ic_generator.stackTypes.append(variable["type"])
            p[0] = p[1], 0

    else:
        raise TypeError(f"'{p[1]}' variable not declared.")


def p_indice(p):
    """indice : lbracket expresion rbracket
              | lbracket expresion rbracket lbracket expresion rbracket
              | empty
    """
    if len(p) > 4:
        p[0] = (p[2], p[5])
    elif len(p) > 2:
        p[0] = (0, p[2])


def p_lbracket(p):
    """lbracket : '['
    """
    ic_generator.stackOperators.append('(')


def p_rbracket(p):
    """rbracket : ']'
    """
    ic_generator.stackOperators.pop()


def p_arreglo(p):
    """arreglo : '[' arregloD ']'
               | arregloD
    """
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_arregloD(p):
    """arregloD : '[' arregloE ']' ',' arregloD
                | '[' arregloE ']'
    """
    if len(p) > 4:
        if p[5][1] != p[2]:
            raise TypeError('Arreglos en misma matriz deben ser de tamaños iguales')
        p[0] = (p[5][0] + 1, p[2])
    else:
        p[0] = (1, p[2])


def p_arregloE(p):
    """arregloE : expresion ',' arregloE
                | expresion
                | empty
    """
    if len(p) > 2:
        p[0] = 1 + p[3]
    else:
        p[0] = 1


def p_funcion_type_id(p):
    """funcion_type_id : type ID
    """
    if not vars_table.initialized:
        vars_table.initialize()

    ic_generator.reset_bases()
    if vars_table.current_scope is not vars_table.table["global"]:
        ic_generator.create_array_size(vars_table.current_scope)
        del vars_table.current_scope["vars"]
    else:
        ic_generator.generate_main_goto()
    vars_table.create_table(p[2], p[1])


def p_funcion_void_id(p):
    """funcion_void_id : void ID
    """
    if not vars_table.initialized:
        vars_table.initialize()

    ic_generator.reset_bases()
    if vars_table.current_scope is not vars_table.table["global"]:
        ic_generator.create_array_size(vars_table.current_scope)
        del vars_table.current_scope["vars"]
    else:
        ic_generator.generate_main_goto()
    vars_table.create_table(p[2], p[1])


def p_funcion(p):
    """funcion : funcion_void
               | funcion_type
    """
    vars_table.current_scope["vars_count"] = len(vars_table.current_scope["vars"])


def p_funcion_void(p):
    """funcion_void : funcion_void_id '(' params r_func_par bloque_void
    """


def p_funcion_type(p):
    """funcion_type : funcion_type_id '(' params r_func_par bloque_return
    """


def p_r_func_par(p):
    """r_func_par : ')'
    """
    vars_table.current_scope["func_begin"] = len(ic_generator.quadrupleList) + 1


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
            size = dope_vector[0] * dope_vector[1]
        else:
            is_array = False
            dope_vector = None
            p_type = p[1]
            size = 1

        address = ic_generator.get_memory_address("local", p_type, size=size)
        vars_table.insert(p[2], p_type, is_array, dope_vector, address)
        vars_table.current_scope["params_type"] += p_type[0]
        vars_table.current_scope["params_count"] += 1


def p_typeA(p):
    """typeA : TYPE_BOOL
            | TYPE_FLOAT
            | TYPE_INT
            | TYPE_STRING
    """
    p[0] = p[1]


def p_type(p):
    """type : typeA
            | typeA '[' INT ']' '[' INT ']'
            | typeA '[' INT ']'

    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 5:
        p[0] = (p[1], (1, int(p[3])))
    else:
        p[0] = (p[1], (int(p[3]), int(p[6])))


def p_error(p):
    # get formatted representation of stack
    if p is None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    raise TypeError(f"Syntax error: Unexpected {token}")


parser = yacc.yacc(start='program')
