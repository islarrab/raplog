class Memory:
    def __init__(self, ofst):        
        self.mem = dict()
        self.offset = ofst
        self.memint = 0
        self.memfloat = 10000
        self.memstr = 20000
        self.membool = 30000

    # 
    def set(self, direccion, value):        
        if self.offset == 200000:
            if type(value) == int:
                rdireccion = self.memint
                self.memint = self.memint + 1
            elif type(value) == float:
                rdireccion = self.memfloat
                self.memflo = self.memflot + 1
            elif type(value) == str:
                rdireccion = self.memstr
                self.memstr = self.memstr + 1
            elif type(value) == bool:
                rdireccion = self.membool
                self.membool = self.membool + 1
                
            self.revisaVacio()
                    
        else:
            rdireccion = direccion - self.offset
                    
        self.mem[rdireccion] = value
        return rdireccion + self.offset

    # Regresa el valor en alguna direccion o imrpime error.
    def read(self, direccion):        
        rdireccion = direccion - self.offset
        if rdireccion in self.mem:
            return self.mem[rdireccion]
        else:
            print "Error en acceso a la memoria"
            exit(1)

    #Revisa si la memoria global esta vacia        
    def revisaVacio(self):        
        flag = 0
        if self.memint >= 10000:
            flag = 1
        if self.memfloat >= 20000:
            flag = 1
        if self.memstr >= 30000:
            flag = 1
        if self.membool >= 40000:
            flag = 1

        if flag == 1:
            print "La memoria esta vacia. Se cerrara el programa."
            exit(1)

    #Regresa de que clase es una direccion
    def mem_class(direccion):
        if direccion >= 200000:             # Resto
            return 4
        if direccion >= 120000:             # Temporal
            return 3
        if direccion >= 80000:              # Constante
            return 2
        if direccion >= 40000:              # Local
            return 1
        return 0                          # Global

    #Regresa el tipo de la variable en enteros
    #0=int 1=float 2=str 3=bool
    def typeNum(t):        
        if t == type(0):
            return 0
        if t == type(0.0):
            return 1
        if t == type(""):
            return 2
        if t == bool:
            return 3

    #Regresa el tipo de una direccion
    def mem_type(direccion):        
        if direccion >= 200000:                # Resto
            direccion = direccion - 200000
        elif direccion >= 120000:              # Temporal
            direccion = direccion - 120000
        elif direccion >= 80000:               # Constante
            direccion = direccion - 80000
        elif direccion >= 40000:               # Local
            direccion = direccion - 40000

        if direccion < 0:
            print "Lo siento pero no existe la memoria negativa:", direccion
            exit(1)

        if direccion < 10000:
            return type(0)            # int
        elif direccion < 20000:
            return type(0.0)          # float
        elif direccion < 30000:
            return type("")           # str
        elif direccion < 40000:
            return bool           # bool
        else:
            return 5
        
