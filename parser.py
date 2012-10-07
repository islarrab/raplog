#!/usr/bin/env python
# file parser.py
import sys

error = False

# Reserved words
reserved = {
   'start' : 'START',
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
	'LPAREN','RPAREN','LCURLY','RCURLY','COMA',
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
t_COMA = r','
#t_NOT = r'(not|NOT|!)'
#t_AND = r'(and|AND|&&)'
#t_OR = r'(or|OR|\|\|)'
t_STR = r'".*"'

def t_INT(t):
	'r[0-9]+'
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
	print("Illegal character '%s'" % t.value[0])
	global error
	error = True
	t.lexer.skip(1)

# Build the lexer 
import lex
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

# tabla de variables
var_table = { }
scopes = [ ]

# tabla de procedimientos
proc_table = { }
current_proc = 'program'

start = 'raplog'

def pop_scope():
    var_table = scopes.pop()

def p_new_scope(p):
    "new_scope :"
    scopes.append(var_table)

def p_add_proc_main(p):
    'add_proc_main :'
    global current_proc
    current_proc = 'main'
    proc_table[current_proc] = {}

def p_set_proc(p):
    'set_proc :'
    global current_proc
    current_proc = p[-1]
    proc_table[current_proc] = {}

def p_raplog(p):
    'raplog : defs add_proc_main START statements-block'

def p_defs(p):
    '''defs : def defs 
            | empty'''

def p_def(p):
    'def : ID set_proc defparams statements-block'

def p_statements_block(p):
    'statements-block : LCURLY new_scope statements RCURLY'
    pop_scope()        # Return to previous scope

def p_statements(p):
    '''statements : assignment statements 
                  | call statements
                  | input statements
                  | output statements
                  | selection statements
                  | loop statements
                  | empty'''

def p_assignment(p):
    'assignment : ID EQ expression'
    var_table[p[1]] = p[3]
    #print 'ID: {}, Proc: {}'.format(p[1], current_proc)
    proc_table[current_proc][p[1]] = p[3]

def p_call(p):
    'call : ID callparams'

def p_input(p):
    'input : GET ID'

def p_output(p):
    'output : PUT string'
    
def p_output_id(p):
    'output : PUT ID'

def p_selection(p):
    '''selection : IF expression statements-block
                 | IF expression statements-block ELSE statements-block'''

def p_loop(p):
    'loop : LOOP expression statements-block'

def p_defparams(p):
    'defparams : LPAREN defparams1 RPAREN'

# para las defparams hay que agregar el caso en el que esten ambas palabras in y out

def p_defparams1(p):
    '''defparams1 : IN ID defparams2 
                  | OUT ID defparams2 
                  | IN OUT ID defparams2 
                  | empty'''
    var_table[p[2]] = 0
    proc_table[current_proc][p[2]] = 0

def p_defparams2(p):
    '''defparams2 : COMA IN ID defparams2 
                  | COMA OUT ID defparams2 
                  | COMA IN OUT ID defparams2 
                  | empty'''
    #var_table[p[3]] = 0
    #proc_table[current_proc][p[3]] = 0

def p_callparams(p):
    'callparams : LPAREN callparams1 RPAREN'

def p_callparams1(p):
    '''callparams1 : expression callparams2 
                   | string callparams2 
                   | empty'''

def p_callparams2(p):
    '''callparams2 : COMA expression callparams2 
                   | COMA string callparams2 
                   | empty'''

def p_varcte_number(p):
    '''varcte : INT 
              | FLOAT'''
    p[0] = p[1]

def p_varcte_id(p):
    'varcte : ID'
    try:
        #p[0] = var_table[p[1]]
        p[0] = proc_table[current_proc][p[1]]
        #print("using: {}, scope: {}".format(p[1], var_table))
    except LookupError:
        print("Undefined variable '{}' at line {}".format(p[1], p.lineno(1)))
        global error
        error = True
        p[0] = 0

def p_string(p):
    'string : STR'
    p[0] = p[1]

'''
def p_string_converter(p):
    'string : expression'
    p[0] = str(p[1])

def p_string_concatenation(p):
    'string : STR PLUS string'
    p[0] = p[1] + p[3]

def p_string_converter_concatenation(p):
    'string : expression PLUS string'
    p[0] = str(p[1]) + p[3]
'''

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

def p_empty(p):
    'empty :'
    pass

def p_error(t):
	print("Syntax error at line {}, near {}".format(t.lineno, t.value))
	global error
	error = True

import yacc
yacc.yacc()

f = open(sys.argv[1], 'r')
yacc.parse(f.read())
if not error:
    print("program has no errors")
