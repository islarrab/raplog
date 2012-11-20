#!/usr/bin/env python
# file symtable.py

import dir

# direcciones virtuales
globaldirs = {int:dir.globint,
              float:dir.globfloat,
              str:dir.globstr,
              bool:dir.globbool}
localdirs = {int:dir.localint,
             float:dir.localfloat,
             str:dir.localstr,
             bool:dir.localbool}
constantdirs = {int:dir.constint,
                float:dir.constfloat,
                str:dir.conststr,
                bool:dir.constbool}
temporaldirs = {int:dir.tempint,
                float:dir.tempfloat,
                str:dir.tempstr,
                bool:dir.tempbool}
pointer_count = 0

maxtemps = {int:0,float:0,str:0,bool:0}

# variable table
'''
una variable tiene el formato {'dir': x, 'type': y, 'dim': z}
por lo tanto var_table tiene el formato:
{  {var1: {'dir': x1, 'type': y1, 'dim': z1},
   ...
   {varN: {'dir': xN, 'type': yN, 'dim': zN} }
'''
var_table = { }
scopes = [ ]

# formato: {valor : {'dir':dir, 'type':type}}
constants = { }

# contadores de variables y temporales, cada procedimiento tiene el suyo propio
var_counter = {int: 0, float:0, bool:0, str:0}
temp_counter = {int: 0, float:0, bool:0, str:0}
const_counter = {int: 0, float:0, bool:0, str:0}

'''
proc_table = {'proc1': {'start_no': #,
						'params': []	,
						'var_table': {}},
			  'proc2': { ... }, ... }
numero de parametros = len(proc_table['params']) 
numero de variables = len(proc_table['var_table'])
'''
proc_table = {'program' : {'start_no':0,
                           'var_counter':var_counter,
                           'temp_counter':temp_counter,
                           'type':None,
                           'params':[],
                           'var_table':var_table}}
current_proc = 'program'


def pop_scope():
    var_table = scopes.pop()

def new_scope():
    scopes.append(var_table)

def reset_locals():
    global localdirs
    global temporaldirs
    localdirs = {int:dir.localint,
                 float:dir.localfloat,
                 str:dir.localstr,
                 bool:dir.localbool}
    temporaldirs = {int:dir.tempint,
                    float:dir.tempfloat,
                    str:dir.tempstr,
                    bool:dir.tempbool}
    


def add_proc(proc_name, start_no, type):
    global current_proc
    global var_table
    global var_counter
    global temp_counter
    global proc_table
    
    # agrega el procedimiento como variable global
    add_var(proc_name, type, None)
    
    reset_locals()
    current_proc = proc_name
    var_counter = {int: 0, float:0, bool:0, str:0}
    temp_counter = {int: 0, float:0, bool:0, str:0}
    var_table = {}
    proc_table[current_proc] = {'start_no':start_no,
                                'var_counter':var_counter,
                                'temp_counter':temp_counter,
                                'type':type,
                                'params':[],
                                'var_table':var_table}

def end_current_proc():
    global current_proc
    global var_table
    global var_counter
    global temp_counter
    current_proc = 'program'
    var_table = proc_table['program']['var_table']
    var_counter = proc_table['program']['var_counter']
    temp_counter = proc_table['program']['temp_counter']

def add_var(name, type, dim):
    var = { 'dir': localdirs[type],
            'type': type,
            'dim': dim }
    var_table[name] = var
    if dim:
        localdirs[type] += dim
        var_counter[type] += dim
    else:
        localdirs[type] += 1
        var_counter[type] += 1
    return var

def add_param(name, type):
    var = { 'dir': localdirs[type],
            'type': type,
            'dim': None }
    proc_table[current_proc]['params'].append(var)
    var_table[name] = var
    localdirs[type] += 1
    var_counter[type] += 1
    return var

def get_proc(proc):
    if proc in proc_table:
        return proc_table[proc]
    else:
        return None

def get_var(name):
    if (name in proc_table[current_proc]['var_table']):
        return proc_table[current_proc]['var_table'][name]
    if (name in proc_table['program']['var_table']):
        return proc_table['program']['var_table'][name]
    return None

def add_constant(value):
    global constants
    if value in constants:
        return constants[value]
    else:
        t = type(value)
        constant = {'dir':constantdirs[t], 'type':t}
        constants[value] = constant
        constantdirs[t] += 1
        const_counter[t] += 1
        return constant

def newtemp(type):
  tempdir = temporaldirs[type]
  temporaldirs[type] += 1
  temp_counter[type] += 1
  return tempdir

def newpointer():
  global pointer_count
  pointer = dir.pointer + pointer_count
  pointer_count += 1
  return pointer
  
def print_symtable():
    for proc in proc_table:
       print(proc+': ')
       for field in proc_table[proc]:
           print('    '+str(field)+' : '+str(proc_table[proc][field]))

