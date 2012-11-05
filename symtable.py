#!/usr/bin/env python
# file symtable.py

# variable table
'''
una variable tiene el formato {'dir': x, 'type': y, 'value': z}
por lo tanto var_table tiene el formato:
{  {var1: {'dir': x1, 'type': y1, 'value': z1},
   ...
   {varN: {'dir': xN, 'type': yN, 'value': zN} }
'''
var_table = { }
scopes = [ ]

# formato: {valor : {'dir':dir, 'type':type}}
constants = { }

'''
proc_table = {'proc1': {'start_no': #,
						'params': []	,
						'var_table': {}},
			  'proc2': { ... }, ... }
numero de parametros = len(proc_table['params']) 
numero de variables = len(proc_table['var_table'])
'''
proc_table = {'program' : {'start_no':1, 'type':None, 'params':[], 'var_table':var_table}}
current_proc = 'program'


def pop_scope():
    var_table = scopes.pop()

def new_scope():
    scopes.append(var_table)

def add_proc(proc_name, start_no, type):
    global current_proc
    current_proc = proc_name
    var_table = {}
    proc_table[current_proc] = {'start_no':start_no,
                                'type':type,
                                'params':[],
                                'var_table':var_table}

def end_current_proc():
    global current_proc
    current_proc = 'program'
    var_table = proc_table['program']['var_table']

def add_var(name, type, value):
    var = { 'dir': name, # TODO: asignar bien la direccion virtual
            'type': type,
            'value': value }
    var_table[name] = var
    return var

def add_param(name, type):
    # TODO: asignar bien 'dir'
    proc_table[current_proc]['params'].append({'name':name, 'dir':name, 'type':type})

def get_proc(proc):
    if proc in proc_table:
        return proc_table[proc]
    else:
        return None

def get_var(name):
    if (name in proc_table[current_proc]['var_table']):
        return proc_table[current_proc]['var_table'][name]
    for param in proc_table[current_proc]['params']:
        if name in param.values():
            return param
    if (name in proc_table[current_proc]['params']):
        return proc_table[current_proc]['params'][name]
    if (name in proc_table['program']['var_table']):
        return proc_table['program']['var_table'][name]
    return None

def add_constant(value):
    if value in constants:
        return constants[value]
    else:
        # TODO: corregir el uso de 'dir'
        constant = {'dir':value, 'type':type(value)}
        constants[value] = constant
        return constant

def print_symtable():
    for proc in proc_table:
       print(proc+': ')
       for field in proc:
           print('    '+str(field))

