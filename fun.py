# -*- coding: cp1252 -*-
#
# Autores: Melissa M. González Mtz. A01087765
#          Isaac Larraguibel Bours A00231505
#
# Clase: Compiladores
# Profesora: Elda Guadalupe Quiroga González
# Fecha: 21 de Noviembre del 2012
#
# Descripción: Esta es la clase Funciones donde se crea la memoria temporal 
# y local de tipo Memoria, asi mismo recibe parametros para las funciones y/o
# un valor
#

from mem import *

class Funciones:
    def __init__(self):
        self.ieje = 0
        self.memlocal = Memoria(40000)
        self.memtemp = Memoria(120000)
        self.param = []
        self.valor = 0    
    
    def setParam(self, direccion, valor, arrtemp, memresto):        
        self.param.append(direccion)
        self.memlocal.set(direccion, valor)
    
    def getParam(self, k):
        return self.param[k]
