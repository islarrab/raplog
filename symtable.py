#!/usr/bin/env python
# file symtable.py

# variable table
var_table = { }
scopes = [ ]

# tabla de procedimientos
# format = {function : [return_type, parameters, var_table]}
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

# adds a variable to current proc
def add_var(name, type, value):
    #print ("adding {"+name+": ["+str(t)+", "+str(value)+"]") 
    global current_proc
    global var_table
    var_table[name] = (type, value)

def get_proc(proc):
    if proc in proc_table:
        return proc_table[proc]
    else:
        return None

def get_var(name):
    if (name in proc_table[current_proc][2]):
        return proc_table[current_proc][2][name]
    if (name in proc_table['program'][2]):
        return proc_table['program'][2][name]
    return None

# looks up the variable in the global and current local scopes, returns boolean
def has(name):
    if (name in proc_table['program'][2] or name in proc_table[current_proc][2]):
        return True
    else:
        return False

def print_symtable():
    for proc in proc_table:
        print '{'+proc+' : '+str(proc_table[proc])+'}'

'''
add_var('var1', 'float', 1.23)
add_proc('one','int',[])
add_var('var2', 'float', 4.56)
print_symtable()
'''
