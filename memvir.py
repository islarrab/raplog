class MemoriaVirtual(object):

    def __init__(self):
        self.memoriaInt = [None] * 1000
        self.memoriaFloat = [None] * 1000
        self.memoriaStr = [None] * 1000
        self.memoriaBool = [None] * 1000
        
    def getMemoriaInt(self, indice):
        return self.memoriaInt[indice]
        
    def getMemoriaFloat(self, indice):
        return self.memoriaFloat[indice]
        
    def getMemoriaStr(self, indice):
        return self.memoriaStr[indice]        

    def getMemoriaBool(self, indice):
        return self.memoriaBool[indice]        

    def setMemoriaInt(self, indice, valor):
        self.memoriaInt[indice] = valor
        
    def setMemoriaFloat(self, indice, valor):
        self.memoriaFloat[indice] = valor
        
    def setMemoriaStr(self, indice, valor):
        self.memoriaStr[indice] = valor        
        
    def setMemoriaBool(self, indice, valor):
        self.memoriaBool[indice] = valor
        
    
