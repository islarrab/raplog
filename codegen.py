#!/usr/bin/env python
# file codegen.py

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
tempno = 0
curr_ins = -1

def newtemp():
  # TODO: cuando definamos bien como manejar las direcciones virtuales
  # hay que arreglar este metodo
  global tempno
  tempno += 1
  return 't'+str(tempno)

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
  # TODO: usar cubo semantico para determinar bien el typo y checar errores
  temp = {'dir':newtemp(), 'type': int}
  gen_quad(oper, opdo1['dir'], '', temp['dir'])
  opdos.append(temp)

def binop(oper):
  opdo2 = opdos.pop()
  opdo1 = opdos.pop()
  # TODO: usar cubo semantico para determinar bien el tipo y checar errores
  temp = {'dir':newtemp(), 'type': int}
  gen_quad(oper, opdo1['dir'], opdo2['dir'], temp['dir'])
  opdos.append(temp)

def write_to_file(file):
  f = open(file, 'w')
  for quad in quads:
    f.write(str(quad)+'\n')
  f.close()

