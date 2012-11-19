#!/usr/bin/env python
# file parser.py
import sys
import lex
import yacc
import symtable
import codegen
import dir

errors = []
lineno = 0
param_counter = 0

# Reserved words
reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'get' : 'GET',
   'put' : 'PUT',
   'and' : 'AND',
   'or' : 'OR',
   'not' : 'NOT',
   'true' : 'TRUE',
   'false' : 'FALSE',
   'return' : 'RETURN',
   'int' : 'TYPEINT',
   'float' : 'TYPEFLOAT',
   'string' : 'TYPESTRING'
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
t_ignore = " \t"
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
    "new_scope :"
    symtable.new_scope()

def p_add_proc(p):
    'add_proc :'
    # TODO: pasar el tipo que regresa y los parametros
    symtable.add_proc(p[-1], codegen.curr_ins+1, p[-2])
# Semantic rules end

def p_raplog(p):
    '''raplog : assignment raplog
              | function raplog'''
    
def p_raplog_empty(p):
    'raplog : empty'

def p_function(p):
    'function : type ID add_proc defparams statements-block'
    symtable.end_current_proc()
    codegen.gen_quad('return', '', '', '')

def p_defparams(p):
    '''defparams : LPAREN defparams1 RPAREN
                 | LPAREN RPAREN'''

def p_defparams1(p):
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
    codegen.gen_quad('return', aux['dir'], '', '')

def p_assignment_expression(p):
    '''assignment : ID EQ expression'''
    exp_res = codegen.opdos.pop()
    print (p[1]+' = '+str(exp_res))
    var = symtable.add_var(p[1], exp_res['type'])
    codegen.gen_quad(p[2], exp_res['dir'], '', var['dir'])

def p_assignment_array(p):
    '''assignment : ID EQ array'''
    # agregar tipo de arreglo para facilitar el manejo
    #var = symtable.add_var(p[1], p[1][
    # TODO: como se manejan los arreglos en cuadruplos?

def p_input(p):
    'input : GET ID'
    var = symtable.get_var(p[2])
    if not var:
      var = symtable.add_var(p[2], str)
    codegen.gen_quad('scan', '', '', var['dir'])

def p_output(p):
    'output : PUT expression'
    aux = codegen.opdos.pop()
    codegen.gen_quad('print', aux['dir'], '', '')

def p_selection(p):
    'selection : IF expression i1 statements-block i3'

def p_selection_else(p):
    'selection : IF expression i1 statements-block ELSE i2 statements-block i3'

def p_i1(p):
    'i1 :'
    aux = codegen.opdos.pop()
    if (aux['type'] != bool and aux['type'] != int):
        errors.append('Line {}: expression must be boolean'.format(lineno))
    codegen.gen_quad(dir.of['gotof'], aux['dir'], '', '')
    codegen.jumps.append(codegen.curr_ins)

def p_i2(p):
    'i2 :'
    codegen.gen_quad('goto', '', '', '')
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
    codegen.gen_quad(dir.of['gotof'], aux['dir'], '', '')
    codegen.jumps.append(codegen.curr_ins)
    
def p_w3(p):
    'w3 :'
    gotof_index = codegen.jumps.pop()
    beginning_index = codegen.jumps.pop()
    codegen.gen_quad(dir.of['goto'], '', '', beginning_index)
    codegen.quads[gotof_index][3] = codegen.curr_ins+1

def p_call(p):
    'call : ID c1 LPAREN callparams RPAREN'
    codegen.gen_quad('gosub', symtable.get_proc(p[1])['start_no'], '', '')
    # reiniciar contador de parametros
    global param_counter
    param_counter = 0
    # devuelve el id para usarse en expresiones
    p[0] = p[1]

def p_c1(p):
    'c1 :'
    proc = symtable.get_proc(p[-1])
    if not proc:
        errors.append("Line {}: Call to an undefined function '{}'".format(p.lineno(1), p[1]))
        raise SyntaxError
    else:
        # TODO: 'era' necesita el tamano total de la funcion, por ahora solo escribe el nombre
        # duda: en la hoja de elda solo viene el nombre, correcto o en realidad va un numero?
        codegen.gen_quad('era',p[-1], '', '')

def p_callparams(p):
    '''callparams : callparams_aux
                  | empty'''

def p_callparams_aux(p):
    '''callparams_aux : callparams_aux COMA expression
                      | expression'''
    global param_counter
    param_counter += 1
    aux = codegen.opdos.pop()
    codegen.gen_quad('param', aux['dir'], '', 'param'+str(param_counter))

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
    print codegen.opdos
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
    print "found true"
    p[0] = symtable.add_constant(1)

def p_varcte_constant_false(p):
    '''varcte : FALSE'''
    p[0] = symtable.add_constant(0)

def p_varcte_id(p):
    '''varcte : ID'''
    var = symtable.get_var(p[1])
    if not var:
        errors.append("Line {}: Undefined variable '{}'".format(p.lineno(1), p[1]))
    else:
        p[0] = var

def p_varcte_id_array(p):
    '''varcte : ID array_index'''
    var = symtable.get_var(p[1])
    if not var:
        errors.append("Line {}: Undefined variable '{}'".format(p.lineno(1), p[1]))
    elif var['type'] != list:
        errors.append("Line {}: Variable '{}' is not an array".format(p.lineno(1), p[1]))
    # TODO: una vez que se arregle la definicion de arreglos hay que 
    # sacar el valor que este en p[2]
    p[0] = var

def p_varcte_function(p):
    '''varcte : call'''
    # TODO: revisar: genera temp nueva y le da el tipo de que regresa la funcion
    p[0] = {'dir':codegen.newtemp(), 'type':symtable.get_proc(p[1])['type']}

def p_array_index(p):
    '''array_index : LBRACK expression RBRACK
                   | LBRACK expression RBRACK array_index'''
    # TODO: cuando se implemente el cubo semantico hay que validar los indices
    #if not isinstance(p[2], (int, long)):
    #    errors.append('Line {}: indices must be integers, not {}'.format(p.lineno(1)))
    # TODO: generacion de codigo

def p_array(p):
    '''array : LBRACK array_elements RBRACK'''
    # TODO: parche temporal, hay que arreglar el uso de arreglos
    
    codegen.opdos.append({'dir':'array', 'type': list})

def p_array_empty(p):
    '''array : LBRACK RBRACK'''
    # TODO: igual que arriba
    codegen.opdos.append({'dir':'array', 'type': list})

def p_array_elements(p):
    '''array_elements : expression'''

def p_array_elements_2(p):
    '''array_elements : expression COMA array_elements'''

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

# Build the parser
yacc.yacc()

# Parse input file
if (len(sys.argv) <= 1):
    print('No file specified, exiting now')
else:
    f = open(sys.argv[1], 'r')
    yacc.parse(f.read())
    if len(errors) > 0:
        if len(errors) == 1: print('found '+str(len(errors))+' error:')
        else:                print('found '+str(len(errors))+' errors:')
        for error in errors:
            print('    '+error)
    else:
        symtable.print_symtable()
        
        # build the actual list to be written to the object file
        # first section, the count of global variables and temporals
        global_counts = symtable.proc_table['program']['var_counter'].values()
        
        
        for quad in codegen.quads:
          print(quad)
        
        
        print('Program has no errors')
        codegen.write_to_file(sys.argv[1].split('.')[0]+'.rlo')
