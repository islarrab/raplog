#!/usr/bin/env python
# -*- coding: cp1252 -*-
#
# Autores: Melissa M. González Mtz. A01087765
#          Isaac Larraguibel Bours A00231505
#
# Clase: Compiladores
# Profesora: Elda Guadalupe Quiroga González
# Fecha: 21 de Noviembre del 2012
#
# Descripción: Es el parser que se encarga de parsear el archivo creado por la
# interfaz, los convierte a cuadruplos para que después sean procesados por
# la máquina virtual
# Valores de entrada : Nombre de archivo
# Valores de salida : Archivo parseado .rlo
#

# file parser.py
import sys
import lex
import yacc
import symtable
import codegen
import dir

errors = []
lineno = 0

# Reserved words
reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'scan' : 'SCAN',
   'print' : 'PRINT',
   'and' : 'AND',
   'or' : 'OR',
   'not' : 'NOT',
   'true' : 'TRUE',
   'false' : 'FALSE',
   'return' : 'RETURN',
   'int' : 'TYPEINT',
   'float' : 'TYPEFLOAT',
   'string' : 'TYPESTRING',
   'def' : 'DEF'
}

tokens = list(reserved.values()) + [
	'PLUS','MINUS','TIMES','DIVIDE',
	'EQ','EQEQ','NE','LT','MT','LTEQ','MTEQ',
	'LPAREN','RPAREN','LCURLY','RCURLY','LBRACK','RBRACK','COMA',
	'INT','FLOAT','STRING','ID'
]

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQ = r'='
t_EQEQ = r'=='
t_NE = r'<>'
t_LT = r'<'
t_MT = r'>'
t_LTEQ = r'<='
t_MTEQ = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_COMA = r','
t_STRING = r'".*"'


def t_FLOAT(t):
	r'[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?'
	
	try:
		t.value = float(t.value)
	except ValueError:
		print("Invalid float value: %s", t.value)
		t.value = 0
	return t

def t_INT(t):
	r'[0-9]+'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Integer value too large: %s", t.value)
		t.value = 0
	return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID') # Check for reserved words
    return t

# Ignored characters
t_ignore = " \t\r"
t_ignore_COMMENT = r'\#.*'

def t_newline(t):
	r'\n+'
	#global lineno
	t.lexer.lineno += t.value.count("\n")
	global lineno
	lineno += t.value.count("\n")

def t_error(t):
	errors.append("Line {}: Illegal character '{}'".format(t.lineno, t.value[0]))
	t.lexer.skip(1)

# Build the lexer 
lex.lex()

# Parsing rules
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('right','NOT'),
    ('nonassoc','EQEQ','NE','LT','MT','LTEQ','MTEQ'),
    ('left','PLUS','MINUS'), 
    ('left','TIMES','DIVIDE'), 
    ('right','UPLUS'),
    ('right','UMINUS')
)


start = 'raplog'

# Semantic rules
def p_new_scope(p):
    'new_scope :'
    symtable.new_scope()

def p_add_proc(p):
    'add_proc :'
    codegen.gen_quad(dir.goto, -1, -1, -1)
    symtable.add_proc(p[-1], codegen.curr_ins+1, int)
    codegen.jumps.append(codegen.curr_ins)
# Semantic rules end

def p_raplog(p):
    '''raplog : function raplog
              | assignment raplog
              | call raplog
              | input raplog
              | output raplog
              | selection raplog
              | while raplog
              | return raplog
              | empty'''

def p_function(p):
    'function : DEF ID add_proc defparams statements-block'
    symtable.end_current_proc()
    codegen.gen_quad(dir.ret, -1, -1, -1)
    codegen.quads[codegen.jumps.pop()][3] = codegen.curr_ins+1

def p_defparams_parens(p):
    '''defparams : LPAREN defparams1 RPAREN
                 | LPAREN RPAREN'''

def p_defparams(p):
    '''defparams1 : type ID 
                  | type ID COMA defparams1'''
    symtable.add_param(p[2], p[1])

def p_statements_block(p):
    'statements-block : LCURLY new_scope statements RCURLY'
    symtable.pop_scope()

def p_statements(p):
    'statements : statement statements'

def p_statements_empty(p):
    'statements : empty'

def p_statement(p):
    '''statement : assignment 
                 | call
                 | input
                 | output
                 | selection
                 | while
                 | return'''

def p_return(p):
    '''return : RETURN expression'''
    aux = codegen.opdos.pop()
    codegen.gen_quad(dir.retorno, aux['dir'], -1, -1)

def p_assignment_expression(p):
    '''assignment : ID EQ expression'''
    exp_res = codegen.opdos.pop()
    var = symtable.add_var(p[1], exp_res['type'], None)
    codegen.gen_quad(dir.asigna, exp_res['dir'], -1, var['dir'])

def p_assignment_index_expression(p):
    '''assignment : ID array_index EQ expression'''
    exp_res = codegen.opdos.pop()
    var = p[2]
    codegen.gen_quad(dir.asigna, exp_res['dir'], -1, var['dir'])

def p_assignment_array(p):
    '''assignment : ID EQ array'''
    array = p[3]
    var = symtable.add_var(p[1], int, len(array))
    for i in range(len(array)):
        codegen.gen_quad(dir.asigna, array[i]['dir'], -1, var['dir']+i)

def p_assignment_array_2(p):
    '''assignment : ID EQ type LBRACK INT RBRACK'''
    var = symtable.add_var(p[1], p[3], p[5])

def p_input(p):
    'input : SCAN ID'
    var = symtable.get_var(p[2])
    if not var:
      var = symtable.add_var(p[2], str, None)
    codegen.gen_quad(dir.scan, -1, -1, var['dir'])

def p_output(p):
    'output : PRINT expression'
    aux = codegen.opdos.pop()
    codegen.gen_quad(dir.printt, aux['dir'], -1, -1)

def p_selection(p):
    'selection : IF expression i1 statements-block i3'

def p_selection_else(p):
    'selection : IF expression i1 statements-block ELSE i2 statements-block i3'

def p_i1(p):
    'i1 :'
    aux = codegen.opdos.pop()
    if (aux['type'] != bool and aux['type'] != int):
        errors.append('Line {}: expression must be boolean'.format(lineno))
    codegen.gen_quad(dir.gotof, aux['dir'], -1, -1)
    codegen.jumps.append(codegen.curr_ins)

def p_i2(p):
    'i2 :'
    codegen.gen_quad(dir.goto, -1, -1, -1)
    i = codegen.jumps.pop()
    codegen.quads[i][3] = codegen.curr_ins+1
    codegen.jumps.append(codegen.curr_ins)

def p_i3(p):
    'i3 :'
    i = codegen.jumps.pop()
    codegen.quads[i][3] = codegen.curr_ins+1

def p_while(p):
    'while : WHILE w1 expression w2 statements-block w3'

def p_w1(p):
    'w1 :'
    codegen.jumps.append(codegen.curr_ins+1)

def p_w2(p):
    'w2 :'
    aux = codegen.opdos.pop()
    if (aux['type'] != bool):
        errors.append('Line {}: expresion must be boolean'.format(lineno))
    codegen.gen_quad(dir.gotof, aux['dir'], -1, -1)
    codegen.jumps.append(codegen.curr_ins)
    
def p_w3(p):
    'w3 :'
    gotof_index = codegen.jumps.pop()
    beginning_index = codegen.jumps.pop()
    codegen.gen_quad(dir.goto, -1, -1, beginning_index)
    codegen.quads[gotof_index][3] = codegen.curr_ins+1

def p_call(p):
    '''call : ID LPAREN callparams RPAREN
            | ID LPAREN noparams RPAREN'''
    # checa si existe la funcion
    proc = symtable.get_proc(p[1])
    if not proc:
        print str(p[1])+' not found!'
        errors.append("Line {}: Call to an undefined function '{}'".format(lineno, p[1]))
        raise SyntaxError
    else:
     codegen.gen_quad(dir.era, -1, -1, -1)
     
     # compara el numero de parametros
     proc_params = proc['params']
     call_params = p[3]
     if len(proc_params) != len(call_params):
         errors.append("Line {}: wrong number of arguments in call to '{}'".format(lineno, p[1]))
         raise SyntaxError
     
     # compara el tipo de parametros, y genera los cuadruplos correspondientes
     for i in range(len(call_params)):
         #if proc_params[i]['type'] != call_params[i]['type']:
         #    errors.append('Line {}: inconsistent parameters in \'{}\''.format(lineno, p[1]))
         #    raise SyntaxError
         codegen.gen_quad(dir.param, call_params[i]['dir'], -1, proc_params[i]['dir'])
     
     codegen.gen_quad(dir.gosub, proc['start_no'], -1, -1)
     
     # devuelve el id para usarse en expresiones
     p[0] = p[1]

def p_noparams(p):
    '''noparams :'''
    p[0] = []

def p_callparams(p):
    '''callparams : expression COMA callparams'''
    aux = codegen.opdos.pop()
    p[0] = [aux] + p[3]

def p_callparams_2(p):
    '''callparams : expression'''
    aux = codegen.opdos.pop()
    p[0] = [aux]

def p_expression_binop(p):
    '''expression : expression AND expression
                  | expression OR expression
                  | expression EQEQ expression
                  | expression NE expression
                  | expression LT expression
                  | expression MT expression
                  | expression LTEQ expression
                  | expression MTEQ expression
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    error = codegen.binop(p[2])
    if error:
        errors.append(error.format(lineno))
        raise SyntaxError

def p_expression_unop_not(p):
    '''expression : NOT expression'''
    error = codegen.unop(p[1])
    if error:
        errors.append(error.format(lineno))
        raise SyntaxError

def p_expression_unop_uplus(p):
    'expression : PLUS expression %prec UPLUS'
    errror = codegen.unop('uplus')
    if error:
        errors.append(error.format(lineno))
        raise SyntaxError

def p_expression_unop_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    error = codegen.unop('uminus')
    if error:
        errors.append(error.format(lineno))
        raise SyntaxError

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'

def p_expression_element(p):
    'expression : varcte'
    codegen.opdos.append(p[1])

def p_varcte_constant(p):
    '''varcte : INT 
              | FLOAT
              | STRING'''
    p[0] = symtable.add_constant(p[1])

def p_varcte_constant_true(p):
    '''varcte : TRUE'''
    p[0] = symtable.add_constant(1)

def p_varcte_constant_false(p):
    '''varcte : FALSE'''
    p[0] = symtable.add_constant(0)

def p_varcte_id(p):
    '''varcte : ID'''
    var = symtable.get_var(p[1])
    if not var:
        errors.append("Line {}: Undefined variable '{}'".format(p.lineno(1), p[1]))
        raise SyntaxError
    else:
        p[0] = var

def p_varcte_id_array(p):
    '''varcte : ID array_index'''
    p[0] = p[2]

def p_varcte_call(p):
    '''varcte : call'''
    var = symtable.proc_table['program']['var_table'][p[1]]
    tempdir = symtable.newtemp(var['type'])
    codegen.gen_quad(dir.asigna, var['dir'], -1, tempdir)
    p[0] = {'dir':tempdir, 'type':var['type']}

def p_array_index(p):
    '''array_index : LBRACK expression RBRACK'''
    var = symtable.get_var(p[-1])
    if not var:
        errors.append("Line {}: Undefined variable '{}'".format(p.lineno(1), p[-1]))
        raise SyntaxError
    elif not var['dim']:
        errors.append("Line {}: Variable '{}' is not an array".format(p.lineno(1), p[-1]))
        raise SyntaxError
    
    exp_res = codegen.opdos.pop()
    if exp_res['type'] != int:
        errors.append("Line {}: Index must be integer:".format(p.lineno(1)))
        raise SyntaxError
    
    liminf = 0
    limsup = var['dim']-1
    codegen.gen_quad(dir.verifica, exp_res['dir'], liminf, limsup)
    basedir = symtable.add_constant(var['dir'])
    pointer = symtable.newpointer()
    codegen.gen_quad(dir.suma, basedir['dir'], exp_res['dir'], pointer)
    p[0] = {'dir':pointer, 'type':int}

def p_array(p):
    '''array : LBRACK array_elements RBRACK'''
    p[0] = p[2]

def p_array_empty(p):
    '''array : LBRACK RBRACK'''
    p[0] = []

def p_array_elements(p):
    '''array_elements : expression'''
    p[0] = [codegen.opdos.pop()]

def p_array_elements_2(p):
    '''array_elements : expression COMA array_elements'''
    p[0] = [codegen.opdos.pop()] + p[3]

def p_type_int(p):
    'type : TYPEINT'
    p[0] = int

def p_type_float(p):
    'type : TYPEFLOAT'
    p[0] = float

def p_type_string(p):
    'type : TYPESTRING'
    p[0] = str

def p_empty(p):
    'empty :'
    pass

def p_error(t):
    errors.append("Line {}: Syntax error near {}".format(t.lineno, t.value))
    # Panic mode: Read ahead looking for a closing '}'
    #while 1:
    #    tok = yacc.token()             # Get the next token
    #    if not tok or tok.type == 'RBRACE': break
    #yacc.restart()

# Build the parser
yacc.yacc()

# Parse input file
if (len(sys.argv) <= 1):
    print('No file specified, exiting now')
else:
    f = open(sys.argv[1], 'r')
    yacc.parse(f.read())
    codegen.gen_quad(-1, -1, -1, -1)
    symtable.print_symtable()
    for quad in codegen.quads:
        print(quad)
    if len(errors) > 0:
        if len(errors) == 1: print('found '+str(len(errors))+' error:')
        else:                print('found '+str(len(errors))+' errors:')
        for error in errors:
            print('    '+error)
    else:
        print('Program has no errors')
        codegen.write_to_file(sys.argv[1].split('.')[0]+'.rlo')
