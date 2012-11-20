#!/usr/bin/env python
# file codegen.py

import semantic_cube
import symtable
import dir

class Node:
  def __init__(self,type,leaf=None,left=None,right=None):
    self.type = type
    self.leaf = leaf
    self.left = left
    self.right = right

opdos = [] # pila de operandos, formato {'dir':dir, 'type':type}
opers = [] # pila de operadores, strings
jumps = [] # pila de saltos, integers
quads = [] # lista de cuadruplos
curr_ins = -1

def gen_quad(oper, opdo1, opdo2, res):
  ''' genera un quadruplo y lo agrega a la lista de cuadruplos
  @param oper el operador del cuadruplo
  @param opdo1 el operando 1 del cuadruplo
  @param opdo2 el operando 2 del cuadruplo
  @param res direccion donde se guarda el resultado de la operacion'''
  global curr_ins
  quads.append([oper, opdo1, opdo2, res])
  curr_ins += 1

def unop(oper):
  opdo1 = opdos.pop()
  newtype = semantic_cube.get_type(oper, opdo1['type'], None)
  if newtype == 'E':
    error = "Line {lineno}: Can't use {oper} on {op1}" 
    return error.format(oper=oper, op1=opdo1['type'])
  temp = {'dir':symtable.newtemp(newtype), 'type': newtype}
  gen_quad(dir.of[oper], opdo1['dir'], '', temp['dir'])
  opdos.append(temp)

def binop(oper):
  opdo2 = opdos.pop()
  opdo1 = opdos.pop()
  newtype = semantic_cube.get_type(oper, opdo1['type'], opdo2['type'])
  if newtype == 'E':
    error = "Line {lineno}: Can't use '{oper}' between {t1} and {t2}" 
    return error.format(lineno='{}', oper=oper, t1=opdo1['type'], t2=opdo2['type'])
  temp = {'dir':symtable.newtemp(newtype), 'type': newtype}
  gen_quad(dir.of[oper], opdo1['dir'], opdo2['dir'], temp['dir'])
  opdos.append(temp)

def peek_opdos():
  return opdos[len(opdos)-1]

def write_to_file(filename):
  f = open(filename, 'w')
  
  # seccion de globales
  #globs = symtable.proc_table['program']['var_counter']
  #f.write(str(globs[int])+' '+str(globs[float])+' '+str(globs[str])+' '+str(globs[bool])+' ')
  
  # seccion de temporales, saca el maximo de temporales de todos los procedimientos
  #t = {int:0, float:0, str:0, bool:0}
  #for proc in symtable.proc_table:
  #  t[int] =   max(t[int],   symtable.proc_table[proc]['temp_counter'][int])
  #  t[float] = max(t[float], symtable.proc_table[proc]['temp_counter'][float])
  #  t[str] =   max(t[str],   symtable.proc_table[proc]['temp_counter'][str])
  #  t[bool] =  max(t[bool],  symtable.proc_table[proc]['temp_counter'][bool])
  #f.write(str(t[int])+' '+str(t[float])+' '+str(t[str])+' '+str(t[bool])+'\n')
  
  # seccion de constantes
  for constant in symtable.constants.keys():
    f.write(str(symtable.constants[constant]['dir'])+' '+str(constant)+'\n')
  
  # divisor
  f.write('---\n')
  
  # seccion de cuadruplos
  for quad in quads:
    for elem in quad:
      f.write(str(elem)+' ')
    f.write('\n')
  f.close()

