class Cuadruplos:

    def __init__(self):
        self.oper = 0
        self.opdo1 = 0
        self.opdo2 = 0
        self.res = 0
        
    def Cuadruplos(self, oper, opdo1, opdo2, res):
            self.oper = oper
            self.opdo1 = opdo1
            self.opdo2 = opdo2
            self.res = res

    def getOper(self):
        return self.oper
    
    def setOper(self,value):
        self.oper = value

    def getOpdo1(self):
        return self.opdo1
    
    def setOpdo1(self,value):
        self.opdo1 = value

    def getOpdo2(self):
        return self.opdo2
    
    def setOpdo2(self,value):
        self.opdo2 = value

    def getRes(self):
        return self.res
    
    def setRes(self,value):
        self.res = value
