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

# tabla de procedimientos
# format = {function : (return_type, parameters, var_table)}
# TODO: falta tamano y dir
RETURN_TYPE = 0; PARAMETERS = 1; VAR_TABLE = 2
proc_table = {'program' : (None, None, var_table)}
current_proc = 'program'


def pop_scope():
    global var_table
    var_table = scopes.pop()

def new_scope():
    global scopes
    scopes.append(var_table)

def add_proc(proc_name, return_type, parameters):
    global current_proc
    global var_table
    global proc_table
    current_proc = proc_name
    var_table = {}
    proc_table[current_proc] = [return_type, parameters, var_table]

def end_current_proc():
    global current_proc
    global var_table
    current_proc = 'program'
    var_table = proc_table['program'][2]

def add_var(name, type, value):
    global var_table
    var = { 'dir': name, # TODO: asignar bien la direccion virtual
            'type': type,
            'value': value}
    var_table[name] = var
    return var

def get_proc(proc):
    if proc in proc_table:
        return proc_table[proc]
    else:
        return None

def get_var(name):
    if (name in proc_table[current_proc][VAR_TABLE]):
        return proc_table[current_proc][VAR_TABLE][name]
    if (name in proc_table['program'][VAR_TABLE]):
        return proc_table['program'][VAR_TABLE][name]
    return None

def get_constant(value):
    if value in constants:
        return constants[value]
    else:
        # TODO: corregir el uso de 'dir'
        constant = {'dir':value, 'type':type(value)}
        constants[value] = constant
        return constant

def print_symtable():
    for proc in proc_table:
        print ('{'+proc+' : '+str(proc_table[proc])+'}')


