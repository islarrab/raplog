from mem import *

"""Class that represents an Activation Record"""
class Funciones:
    def __init__(self):
        self.ieje = 0
        self.memlocal = Memory(40000)
        self.memtemp = Memory(120000)
        self.param = []
        self.return_value = 0
    
    
    
    def setParam(self, address, value, past_ar, mwild):
        if type(value) == type([]):
            for i in range(len(value)):
                elem = value[i]
                if mem_type(elem) == type([]):                  # If 150001 or 203001
                    value[i] = self.swap_memories(elem, past_ar, mwild)
        
        self.param.append(address)
        self.memlocal.set(address, value)   
    
    def getParam(self, k):
        return self.param[k]
