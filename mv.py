#!/usr/bin/env python
# -*- coding: cp1252 -*-

import cuadruplos
import memvir
import regmem
import proc
import stack

class MV(object):    

    def __init__(self):
        self.mv = memvir.MemoriaVirtual()  # same as doing it in another class
        self.cuad = cuadruplos.Cuadruplos()
        self.rm = regmem.RegistroMemoria()
        self.pr = proc.Procedimiento()
        self.stack = stack.Stack()
        self.memoria = [self.mv]
        self.cuadruplos = [(self.cuad)]
        self.directorio = [None] * 10000
        self.ieje = 0
        self.stackeje = [self.stack]
        self.param = [None]
    
    def getIndiceEjecucion(self):
        return self.ieje

    def getTotalCuad(self):
        return len(self.cuadruplos)

    def getCuadruplo(self):
        return self.cuadruplos[self.ieje]

    #Descripción: Constructor que crea una maquina virtual vacia
    
    # Descripción: Constructor que crea una maquina virtual con su directorio, su memoria virtual, su lista de cuadruplos, stack de ejecucion vacio
    # Leé del código objeto
    # Entrada: fileLocation
    def MaqVir(self, fileName):
            self.directorio = []
            self.memoria = [self.mv for x in range(4)]
            self.cuadruplos = [(self.cuad)]
            self.stackeje = [self.stack]
            self.ieje = 0
            auxlinea = ""

            #Lectura del Archivo del codigo Objeto
            f = open(fileName, "r")
            #Primera linea
            linea = f.readline()
            linea = linea.replace('[','')
            linea = linea.replace(']','')
            #Lectura de cuadruplos
            while True:
                if not linea: break
                c = linea.split(',');
                cuadruplo = self.cuad.Cuadruplos(c[0], c[1], c[2], c[3]);
                self.cuadruplos.append(cuadruplo);

                #Siguiente linea
                linea = f.readline()
                linea = linea.replace('[','')
                linea = linea.replace(']','')

    #Descripción: Método de instancia el cual nos indica si es posible o no ejecutar un cuadruplo en la Maquina virtual
    def permiteEjecutar(self):
        if (self.getTotalCuad() > 0) and (self.ieje != self.getTotalCuad()):
            return True
        else:
            return False

    #Descripción: Método de instancia el cual ejecuta el siguiente cuadruplo y escribe el objeto MensajeCuadruplo con la información de regreso
    #Entrada: Cuadruplos cuad, MensajeCuadruplo retorno
    def ejecutaCuadruplo(self, cuad, retorno):
        tm=0
        tm1=0
        tm2=0
        tipo=0
        tipo1=0
        tipo2=0
        offset1=0
        offset2=0
        boolval = False
        
        reg_pasado = self.stackeje.stack.Peek();
        if not (reg_pasado.rm.Ready()):
            reg_pasado = self.stackeje[1]
        a=cuad.cuad.getOper()
        if(a==1 or a==3): #suma
            tm1 = (cuad.self.cuad.getOpdo1() / 100000) - 1
            tm2 = (cuad.self.cuad.getOpdo2() / 100000) - 1
            tipo1 = (cuad.self.cuad.getOpdo1() / 10000) % 10
            tipo2 = (cuad.self.cuad.getOpdo2() / 10000) % 10

            # Se obtiene el offset del pasado
            if tm1 == 1:
                offset1 = reg_pasado.self.rm.offsetLocal[tipo1-1];
            elif tm1 == 2:
                offset1 = reg_pasado.self.rm.offsetTemporal[tipo1-1];
            if tm2 == 1:
                offset2 = reg_pasado.self.rm.offsetLocal[tipo2-1];
            elif tm2 == 2:
                offset2 = reg_pasado.self.rm.offsetTemporal[tipo2-1];

            if tipo1 == 1:
                if tipo2 == 1:
                    valor = self.memoria[tm1].self.mv.getMemoriaInt((cuad.self.cuad.getOpdo1() % 10000)+offset1) + self.memoria[tm2].self.mv.getMemoriaInt((cuad.self.cuad.getOpdo2() % 10000)+offset2)
                    guarda_en_memoria(not self.stackeje.stack.Peek().rm.Ready(), cuad.self.cuad.getRes(), valor)
                elif tipo2 == 2:
                    valor = self.memoria[tm1].self.mv.getMemoriaInt((cuad.self.cuad.getOpdo1() % 10000)+offset1) + self.memoria[tm2].self.mv.getMemoriaFloat((cuad.self.cuad.getOpdo2() % 10000)+offset2)
                    guarda_en_memoria(not self.stackeje.stack.Peek().rm.Ready(), cuad.self.cuad.getRes(), valor)
            elif tipo1 == 2:
                if tipo2 == 1:
                    valor = self.memoria[tm1].self.mv.getMemoriaFloat((cuad.self.cuad.getOpdo1() % 10000)+offset1) + self.memoria[tm2].self.mv.getMemoriaInt((cuad.self.cuad.getOpdo2() % 10000)+offset2)
                    guarda_en_memoria(not self.stackeje.stack.Peek().rm.Ready(), cuad.self.cuad.getRes(), valor)
                elif tipo2 == 2:
                    valor = self.memoria[tm1].self.mv.getMemoriaFloat((cuad.self.cuad.getOpdo1() % 10000) + offset1) + self.memoria[tm2].self.mv.getMemoriaFloat((cuad.self.cuad.getOpdo2() % 10000)+offset2)
                    guarda_en_memoria(not self.stackeje.stack.Peek().rm.Ready(), cuad.self.cuad.getRes(), valor)
            self.ieje= self.ieje + 1            

    #Descripción: Método de instancia el cual guarda el valor, en la dirección virtual, de la memoria en el contexto que depende del param
    #Entrada: param, direccion_virtual, valor
    def guarda_en_memoria(self, param, direccion_virtual, valor):
        tipomemoria = (direccion_virtual / 100000)-1
        direccion_virtual %= 100000
        tipovalor = direccion_virtual / 10000
        direccion_virtual %= 10000
        offset = 0
            
        reg_pasado = self.stackeje.stack.Peek();
        if (param):
            reg_pasado = self.stackeje[1]
        if tipomemoria == 1:
            offset = reg_pasado.rm.offsetLocal[tipovalor - 1]
        elif tipomemoria == 2:
            offset = reg_pasado.rm.offsetTemporal[tipovalor - 1]
        result = {
            '1': self.memoria[tipomemoria].mv.setMemoriaInt(direccion_virtual + offset, valor),
            '2': self.memoria[tipomemoria].mv.setMemoriaFloat(direccion_virtual + offset, valor),
            '3': self.memoria[tipomemoria].mv.setMemoriaStr(direccion_virtual + offset, valor),
            '4': self.memoria[tipomemoria].mv.setMemoriaBool(direccion_virtual + offset, (valor is "true"))
        }[tipovalor]

    # Descripción: Método de instancia el cual nos indica si el registro de memoria de la funcion esta listo.
    def registro_listo(self):
        return self.stackeje.stack.Peek().rm.Ready();
