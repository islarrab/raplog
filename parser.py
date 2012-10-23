#!/usr/bin/env python
# file parser.py
import sys
import lex
import yacc
import symtable
import codegen

errors = []

# Reserved words
reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'in' : 'IN',
   'out' : 'OUT',
   'get' : 'GET',
   'put' : 'PUT',
   'not' : 'NOT',
   'and' : 'AND',
   'or' : 'OR'
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
#t_NOT = r'(not|NOT|!)'
#t_AND = r'(and|AND|&&)'
#t_OR = r'(or|OR|\|\|)'
t_STRING = r'".*"'

def t_INT(t):
	r'[0-9]+'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Integer value too large: %s", t.value)
		t.value = 0
	return t

def t_FLOAT(t):
	r'[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
	try:
		t.value = float(t.value)
	except ValueError:
		print("Invalid float value: %s", t.value)
		t.value = 0
	return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    
    t.type = reserved.get(t.value,'ID') # Check for reserved words
    if t.value == 'true':
        t.value = True
    elif t.value == 'false':
        t.value = False
    return t

# Ignored characters
t_ignore = " \t"
t_ignore_COMMENT = r'\#.*'

def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")

def t_error(t):
	global errors
	errors.append("Illegal character '{}' at line {}".format(t.value[0], t.lineno))
	t.lexer.skip(1)

# Build the lexer 
lex.lex()
'''
lex.input(open(sys.argv[1], 'r').read())
while 1:
    tok = lex.token()
    if not tok:
        break
    print (tok)
'''
# Parsing rules
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('nonassoc','EQEQ','NE','LT','MT','LTEQ','MTEQ'),
    ('left','PLUS','MINUS'), 
    ('left','TIMES','DIVIDE'), 
    ('right','NOT'),
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
    symtable.add_proc(p[-1], None, None)
# Semantic rules end

def p_raplog(p):
    '''raplog : assignment raplog
              | function raplog'''
    p[0] = [p[1]] + p[2]
    
def p_raplog_empty(p):
    'raplog : empty'
    p[0] = []

def p_function(p):
    'function : ID add_proc defparams statements-block'
    symtable.end_current_proc()
    # TODO: hacer algo con defparams
    p[0] = p[4]

def p_statements_block(p):
    'statements-block : LCURLY new_scope statements RCURLY'
    symtable.pop_scope()
    p[0] = p[3]

def p_statements(p):
    'statements : statement statements'
    p[0] = [p[1]] + p[2]

def p_statements_empty(p):
    'statements : empty'
    p[0] = []

def p_statement(p):
    '''statement : assignment 
                 | call
                 | input
                 | output
                 | selection
                 | while'''
    p[0] = p[1]

def p_assignment_expression(p):
    '''assignment : ID EQ expression'''
    # TODO: revisar bien porque usar p[3].type en vez de type(p[3]) marca error
    symtable.add_var(p[1], type(p[3]), p[3])
    p[0] = codegen.Node('assignment', p[2], codegen.Node(type(p[3]), p[1], None, None), p[3])

def p_assignment_array(p):
    '''assignment : ID EQ array'''
    symtable.add_var(p[1], list, p[3])
    p[0] = codegen.Node('assignment', p[2], codegen.Node(list, p[1], None, None), p[3])

def p_call(p):
    'call : ID callparams'
    symtable.get_proc(p[1])
    p[0] = codegen.Node('call', p[1], None, None)
    # TODO: checar existencia y manejar parametros

def p_input(p):
    'input : GET ID'
    if not symtable.has(p[2]):
      # TODO: es posible que se necesite agregar el tipo de una vez
      symtable.add_var(p[2], None, None)
    p[0] = codegen.Node('input', 'scan', codegen.Node(p[2], None, None), None)

def p_output(p):
    'output : PUT expression'
    p[0] = codegen.Node('output', 'print', p[2], None)

def p_selection(p):
    'selection : IF expression statements-block'
    p[0] = codegen.Node('if', p[1], p[2], p[3])

def p_selection_else(p):
    'selection : IF expression statements-block ELSE statements-block'
    p[0] = codegen.Node('if', p[1], p[2], codegen.Node('else', p[4], p[3], p[5]))

def p_while(p):
    'while : WHILE expression statements-block'
    p[0] = codegen.Node('while', 'while', p[2], p[3])

def p_defparams(p):
    '''defparams : LPAREN defparams1 RPAREN
                 | LPAREN RPAREN'''
    # TODO: generacion de codigo

def p_defparams1(p):
    '''defparams1 : param_type ID 
                  | param_type ID COMA defparams1'''
    # TODO: determinar si si es aceptable el IN OUT ID, por ahora no es aceptado
    # TODO: assignar el valor correcto de los parametros
    symtable.add_var(p[2], int, 0)
    # TODO: generacion de codigo

def p_param_type(p):
    '''param_type : IN
                  | OUT'''
    # TODO: generacion de codigo
    p[0] = []

def p_callparams(p):
    'callparams : LPAREN callparams1 RPAREN'
    # TODO: generacion de codigo
    p[0] = []

def p_callparams1(p):
    '''callparams1 : expression callparams2 
                   | empty'''
    # TODO: generacion de codigo
    p[0] = []

def p_callparams2(p):
    '''callparams2 : COMA expression callparams2 
                   | empty'''
    # TODO: generacion de codigo
    p[0] = []

# TODO: hacer uso del cubo semantico en las expresiones
def p_expression_boolean(p):
    '''expression : expression AND expression
                  | expression OR expression'''
    p[0] = codegen.Node(bool, p[2], p[1], p[3])

def p_expression_boolean_not(p):
    '''expression : NOT expression'''
    p[0] = codegen.Node(bool, p[1], p[2], None)

def p_expression_comparison(p):
    '''expression : expression EQEQ expression
                  | expression NE expression
                  | expression LT expression
                  | expression MT expression
                  | expression LTEQ expression
                  | expression MTEQ expression'''
    p[0] = codegen.Node(bool, p[2], p[1], p[3])

def p_expression_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = codegen.Node(None, p[2], p[1], p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_uplus(p):
    'expression : PLUS expression %prec UPLUS'
    p[0] = p[2]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = codegen.Node(p[2].type, 'uminus', p[2], None)

def p_expression_element(p):
    'expression : varcte'
    p[0] = p[1]

def p_varcte_constant(p):
    '''varcte : INT 
              | FLOAT
              | STRING'''
    p[0] = codegen.Node('leaf', p[1], None, None)

def p_varcte_id(p):
    '''varcte : ID'''
    # TODO: uso apropiado de id en el nodo
    var = symtable.get_var(p[1])
    if not var:
        global errors
        errors.append("Undefined variable '{}' at line {}".format(p[1], p.lineno(1)))
    else:
        p[0] = codegen.Node(var[0], p[1], None, None)

def p_varcte_id_array(p):
    '''varcte : ID array_index'''
    # TODO: validacion apropiada para arreglos
    # TODO: uso apropiado de id en el nodo
    var = symtable.get_var(p[1])
    global errors
    if not var:
        errors.append("Undefined variable '{}' at line {}".format(p[1], p.lineno(1)))
    elif var[0] != list:
        errors.append("Variable '{}' is not an array, at line {}".format(p[1], p.lineno(1)))
    # TODO: una vez que se arregle la definicion de arreglos hay que sacar el valor
    # que este en p[2]
    p[0] = codegen.Node(var[0], p[1], None, None)


def p_array_index(p):
    '''array_index : LBRACK expression RBRACK
                   | LBRACK expression RBRACK array_index'''
    # TODO: cuando se implemente el cubo semantico hay que validar los indices
    #if not isinstance(p[2], (int, long)):
    #    global errors
    #    errors.append('Wrong index type at line {}, indexes must be integers'.format(p.lineno(1)))
    # TODO: generacion de codigo

def p_array(p):
    '''array : LBRACK array_elements RBRACK'''
    #p[0] = codegen.Node(list, p[2], None, None)
    p[0] = codegen.Node('array', p[2], None, None)

def p_array_empty(p):
    '''array : LBRACK RBRACK'''
    p[0] = codegen.Node(list, [], None, None)

def p_array_elements(p):
    '''array_elements : expression'''
    p[0] = [p[1]]

def p_array_elements_2(p):
    '''array_elements : expression COMA array_elements'''
    p[0] = [p[1]] + p[3]

def p_empty(p):
    'empty :'
    pass

def p_error(t):
	global errors
	errors.append("Syntax error at line {}, near {}".format(t.lineno, t.value))

# Build the parser
yacc.yacc()

# Parse input file
if (len(sys.argv) <= 1):
    print('No file specified, exiting now')
else:
    f = open(sys.argv[1], 'r')
    result = yacc.parse(f.read())
    if len(errors) > 0:
        print('found '+str(len(errors))+' errors:')
        for error in errors:
            print('    '+error)
    else:
        print('Program has no errors')
        #codegen.print_ast(result)
        print(result)
        vp = codegen.gen_incode(result)
        print(str(vp))
        codegen.write_to_file(vp, sys.argv[1].split('.')[0]+'.rpo')
