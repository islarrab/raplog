#!/usr/bin/env python
# file codegen.py

class Node:
  def __init__(self,leaf=None,left=None,right=None):
    self.leaf = leaf
    self.left = left
    self.right = right

# Abstract Syntax Tree
vp = []
quads = []

def gen_vp(ast):
  for item in ast:
    if isinstance(item, list):
      gen_vp(item)
    else:
      postorder(item)
  return vp

def postorder(node):
  global vp
  if not node:
    return
  if isinstance(node, list):
    gen_vp(node)
    return
  postorder(node.left) 
  postorder(node.right)
  vp.append(node.leaf)

''' #while in vp
p[0] = [
        codegen.Node('L1:', None, None),
        codegen.Node('gotof', p[2], codegen.Node('L2', None, None)),
        p[3],
        codegen.Node('goto', codegen.Node('L1', None, None), None)
    ]
'''

def generate_quads(node):
  return
