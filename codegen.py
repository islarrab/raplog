#!/usr/bin/env python
# file codegen.py

class Node:
  def __init__(self,type,leaf=None,left=None,right=None):
    self.type = type
    self.leaf = leaf
    self.left = left
    self.right = right

vp = []
quads = []
labelno = 0

def newlabel():
  global labelno
  labelno = labelno + 1
  return 'L'+str(labelno)

def gen_exp(node, vp):
  if not node:
    return
  gen_exp(node.left, vp)
  gen_exp(node.right, vp)
  vp.append(node.leaf)
  return vp

def gen_if(node):
  l1 = newlabel()
  vp = []
  if isinstance(node.right, Node):
    # if has else
    l2 = newlabel()
    vp = gen_exp(node.left, []) \
       + [l1, 'gotof'] \
       + gen_incode(node.right.left) \
       + [l2, 'goto', l1+':'] \
       + gen_incode(node.right.right) \
       + [l2+':']
  else:
    # if has no else
    vp = gen_exp(node.left, []) \
       + [l1, 'gotof'] \
       + gen_incode(node.right) \
       + [l1+':']
  return vp

def gen_while(node):
  l1 = newlabel()
  l2 = newlabel()
  vp = [l1+':'] \
     + gen_exp(node.left, []) \
     + [l2, 'gotof'] \
     + gen_incode(node.right)
  return vp

def gen_incode(ast):
  vp = []
  for statement in ast:
    if isinstance(statement, list):
      vp = vp + gen_incode(statement)
    elif statement.type == 'if':
      vp = vp + gen_if(statement)
    elif statement.type == 'while':
      vp = vp + gen_while(statement)
    else:
      vp = vp + gen_exp(statement, [])
  return vp

def write_to_file(code, file):
  f = open(file, 'w')
  for elem in code:
    f.write(str(elem)+' ')
  f.close()

def print_ast(node, indent=''):
  if not node:
    return
  if isinstance(node, list):
    for item in node:
      print_ast(item, indent)
    return
  print(indent+str(node.leaf))
  print_ast(node.left, indent+'  ')
  print_ast(node.right, indent+'  ')

def print_true_ast(node, indent=''):
  if not node:
    return
  print(indent+str(node.leaf))
  print_ast(node.left, indent+'  ')
  print_ast(node.right, indent+'  ')

