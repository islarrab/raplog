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
