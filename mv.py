import cuadruplos
import memvir
import regmem
import proc
import stack

class MV(object):
    

    mv = memvir.MemoriaVirtual()  # same as doing it in another class
    cuad = cuadruplos.Cuadtruplos()
    rm = regmem.RegistroMemoria()
    stack = stack.Stack()
    memoria = [mv]
    cuadruplos = [(cuad)]
    directorio = [None] * 10000
    ieje = 0
    stackeje = [stack]
    param = [None]
    
    def getIndiceEjecucion():
        return ieje

    def getTotalCuad():
        return len(cuadruplos)

    def getCuadruplo():
        return cuadruplos[ieje]

    #Descripción: Constructor que crea una maquina virtual vacia

    def MV():
        cuadruplos = [(cuad)]

    # Descripción: Constructor que crea una maquina virtual con su directorio, su memoria virtual, su lista de cuadruplos, stack de ejecucion vacio
    #              Leé del código objeto
    # Entrada: string file_location
    def MV(fileLocation)
            directorio = [None] * 10000
            memoria = [mv for x in range(4)]
            cuadruplos = [(cuad)]
            stackeje = [stack]
            ieje = 0
            #codigo para leer el archivo de codigo objeto

     #Descripción: Método de instancia el cual nos indica si es posible o no ejecutar un cuadruplo en la Maquina virtual
    def permiteEjecutar():
        if self.totalCuad > 0 && ieje != self.totalCuad:
            return true
        else:
            return false

       #Descripción: Método de instancia el cual ejecuta el siguiente cuadruplo y escribe el objeto MensajeCuadruplo con la información de regreso
       #Entrada: Cuadruplos cuad, MensajeCuadruplo retorno

    def ejecutaCuadruplo(cuad, retorno):
        tm=0
        tm1=0
        tm2=0
        tipo=0
        tipo1=0
        tipo2=0
        offset1=0
        offset2=0
        boolval = false
        
        reg_pasado = stackeje.stack.Peek();
        if !reg_pasado.rm.Ready:
            reg_pasado = stackeje[1]
        result = {
            '1': 
            '3': tm1 = (cuad.cuad.opdo1 / 100000) - 1
                 tm2 = (cuad.cuad.opdo2 / 100000) - 1
                 tipo1 = (cuad.cuad.opdo1 / 10000) % 10
                 tipo2 = (cuad.cuad.opdo2 / 10000) % 10

                 # Se obtiene el offset del pasado
                 if tm1 == 1:
                     offset1 = reg_pasado.rm.offsetLocal[tipo1-1];
                 else if tm1 == 2:
                     offset1 = reg_pasado.rm.offsetTemporal[tipo1-1];
                 if tm2 == 1:
                     offset2 = reg_pasado.rm.offsetLocal[tipo2-1];
                 else if tm2 == 2:
                     offset2 = reg_pasado.rm.offsetTemporal[tipo2-1];

                 if tipo1 == 1:
                     if tipo2 == 1:
                         valor = memoria[tm1].getMemoriaInt((cuad.cuad.getOpdo1 % 10000)+offset1) + memoria[tm2].getMemoriaInt((cuad.cuad.getOpdo2 % 10000)+offset2)
                         guarda_en_memoria(!stackeje.stack.Peek().rm.Ready(), cuad.cuad.getRes(), valor)
                     else if tipo2 == 2:
                         valor = memoria[tm1].getMemoriaInt((cuad.cuad.getOpdo1 % 10000)+offset1) + memoria[tm2].getMemoriaFloat((cuad.cuad.getOpdo2 % 10000)+offset2)
                         guarda_en_memoria(!stackeje.stack.Peek().rm.Ready, cuad.cuad.getRes(), valor)
                 else if tipo1 == 2:
                     if tipo2 == 1:
                         valor = memoria[tm1].getMemoriaFloat((cuad.cuad.getOpdo1 % 10000)+offset1) + memoria[tm2].getMemoriaInt((cuad.cuad.getOpdo2 % 10000)+offset2)
                         guarda_en_memoria(!stackeje.stack.Peek().rm.Ready, cuad.cuad.getRes(), valor)
                     else if tipo2 == 2:
                         valor = memoria[tm1].getMemoriaFloat((cuad.cuad.getOpdo1 % 10000) + offset1) + memoria[tm2].getMemoriaFloat((cuad.cuad.getOpdo2 % 10000)+offset2)
                         guarda_en_memoria(!stackeje.stack.Peek().rm.Ready, cuad.cuad.getRes(), valor)
                 ieje++,
            '2':          
        }[cuad.cuad.getOper]

                    

    #Descripción: Método de instancia el cual guarda el valor, en la dirección virtual, de la memoria en el contexto que depende del param
    #Entrada: param, direccion_virtual, valor
    def guarda_en_memoria(param, direccion_virtual, valor):
        tipomemoria = (direccion_virtual / 100000)-1
        direccion_virtual %= 100000
        tipovalor = direccion_virtual / 10000
        direccion_virtual %= 10000
        offset = 0
            
        reg_pasado = stackeje.stack.Peek();
        if (param):
            reg_pasado = stackeje[1]
        if tipomemoria == 1:
            offset = reg_pasado.rm.offsetLocal[tipovalor - 1]
        else if tipomemoria == 2:
            offset = reg_pasado.rm.offsetTemporal[tipovalor - 1]
        result = {
            '1': memoria[tipomemoria].mv.setMemoriaInt(direccion_virtual + offset, valor),
            '2': memoria[tipomemoria].mv.setMemoriaFloat(direccion_virtual + offset, valor),
            '3': memoria[tipomemoria].mv.setMemoriaStr(direccion_virtual + offset, valor),
            '4': memoria[tipomemoria].mv.setMemoriaBool(direccion_virtual + offset, (valor is "true"))
        }[tipovalor]

    # Descripción: Método de instancia el cual nos indica si el registro de memoria de la funcion esta listo.
    def registro_listo():
        return stackeje.stack.Peek().rm.Ready();
