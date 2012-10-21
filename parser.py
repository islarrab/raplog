#!/usr/bin/env python
# file parser.py
import sys
import lex
import yacc
import symtable

errors = []

# Reserved words
reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'loop' : 'LOOP',
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
	'INT','FLOAT','STR','ID'
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
t_STR = r'".*"'

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
    print tok
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

def p_add_proc_main(p):
    'add_proc_main :'
    symtable.add_proc('main')

def p_add_proc(p):
    'add_proc :'
    # TODO: pasar el tipo que regresa y los parametros
    symtable.add_proc(p[-1], None, None)
# Semantic rules end

def p_raplog(p):
    '''raplog : assignment raplog
              | function raplog
              | empty'''

def p_function(p):
    'function : ID add_proc defparams statements-block'
    symtable.end_current_proc()

def p_statements_block(p):
    'statements-block : LCURLY new_scope statements RCURLY'
    symtable.pop_scope()

def p_statements(p):
    '''statements : statement statements
                  | empty'''

def p_statement(p):
    '''statement : assignment 
                 | call
                 | input
                 | output
                 | selection
                 | loop'''

def p_assignment(p):
    '''assignment : ID EQ expression
                  | ID EQ array'''
    symtable.add_var(p[1], type(p[3]), p[3])

def p_call(p):
    'call : ID callparams'
    p[0] = symtable.get_proc(p[1])
    # TODO: checar existencia y manejar parametros

def p_input(p):
    'input : GET ID'

def p_output(p):
    'output : PUT expression'

def p_selection(p):
    '''selection : IF expression statements-block
                 | IF expression statements-block ELSE statements-block'''

def p_loop(p):
    'loop : LOOP expression statements-block'

def p_defparams(p):
    '''defparams : LPAREN defparams1 RPAREN
                 | LPAREN RPAREN'''

def p_defparams1(p):
    '''defparams1 : param_type ID 
                  | param_type ID COMA defparams1'''
    # TODO: determinar si si es aceptable el IN OUT ID
    # TODO: assignar el valor correcto de los parametros
    symtable.add_var(p[2], 'int', 0)

def p_param_type(p):
    '''param_type : IN
                  | OUT'''

def p_callparams(p):
    'callparams : LPAREN callparams1 RPAREN'

def p_callparams1(p):
    '''callparams1 : expression callparams2 
                   | empty'''

def p_callparams2(p):
    '''callparams2 : COMA expression callparams2 
                   | empty'''

def p_varcte_constant(p):
    '''varcte : INT 
              | FLOAT
              | STR'''
    p[0] = p[1]

def p_varcte_id(p):
    '''varcte : ID
              | ID array_index'''
    # TODO: validacion apropiada para arreglos
    p[0] = symtable.get_var(p[1])
    if not p[0]:
        global errors
        errors.append("Undefined variable '{}' at line {}".format(p[1], p.lineno(1)))

def p_expression_boolean(p):
    '''expression : expression AND expression
                  | expression OR expression
                  | NOT expression'''

def p_expression_comparison(p):
    '''expression : expression EQEQ expression
                  | expression NE expression
                  | expression LT expression
                  | expression MT expression
                  | expression LTEQ expression
                  | expression MTEQ expression'''

def p_expression_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_uplus(p):
    'expression : PLUS expression %prec UPLUS'
    p[0] = p[2]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_element(p):
    'expression : varcte'
    p[0] = p[1]

def p_array_index(p):
    '''array_index : LBRACK expression RBRACK
                   | LBRACK expression RBRACK array_index'''
    if not isinstance(p[2], (int, long)):
        global errors
        errors.append('Wrong index type at line {}, indexes must be integers'.format(p.lineno(1)))

def p_array(p):
    '''array : LBRACK array_elements RBRACK
             | LBRACK RBRACK'''

def p_array_elements(p):
    '''array_elements : expression
                      | expression COMA array_elements'''

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
    yacc.parse(f.read())
    if len(errors) > 0:
        print 'found '+str(len(errors))+' errors:'
        for error in errors:
            print '    '+error
    else:
        print('Program has no errors')

