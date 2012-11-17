#!/usr/bin/env python
# -*- coding: cp1252 -*-

import sys
import os
from memory import *
#import cuadruplos
import regmem
import proc
import stack

#cuad = cuadruplos.Cuadruplos()
rm = regmem.RegistroMemoria()
pr = proc.Procedimiento()
stack = stack.Stack()
memglobal = Memory(0)
memlocal = Memory(40000)
memconst = Memory(80000)
memtemp = Memory(120000)
memresto = Memory(200000)
cuadruplos = []
ieje = 0
stackeje = [stack]
param = []

def getIndiceEjecucion():
    return ieje

def getTotalCuad():
    return len(cuadruplos)

def getCuadruplo():
    return cuadruplos[ieje]

def cargarArchivo(fileName):
        directorio = []
        stackeje = [stack]
        ieje = 0
        auxlinea = ""

        #Lectura del Archivo del codigo Objeto
        f = open(fileName, "r")        
        #Primera linea
        linea = f.readline()        
        #Lectura de memoria
        while(linea != '---\n'):
            #Lectura de constantes
            c = linea.split()
            #checando tipo de la constante
            t = memglobal.mem_type(int(c[0]))
            guarda_en_memoria(int(c[0]),t(c[1]))
            linea = f.readline()
        #Lectura de cuadruplos
        linea = f.readline()
        while True:
            if not linea: break
            c = [int(n) for n in linea.split()]
            #cuadruplo = cuad.Cuadruplos(c[0], cuad[1], cuad[2], cuad[3])
            cuadruplos.append(c)
            #Siguiente linea
            linea = f.readline()
            

#Descripción: Método de instancia el cual nos indica si es posible o no ejecutar un cuadruplo en la Maquina virtual
def permiteEjecutar():
    if (getTotalCuad() > 0) and (ieje != getTotalCuad()):
        return True
    else:
        return False

#Descripción: Método de instancia el cual ejecuta el siguiente cuadruplo y escribe el objeto MensajeCuadruplo con la información de regreso
#Entrada: cuad
def ejecutaCuadruplos():
    global ieje
    while ieje < getTotalCuad():
        cuad = cuadruplos[ieje]
        op= cuad[0]
        
        if op == 0: # suma
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1+v2)

        elif op == 1: #resta
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1-v2)
            
        elif op == 2: #multiplicacion
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1*v2)
            
        elif op == 3: #division
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1/v2)
            
        elif op == 4: #menor que
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1<v2)

        elif op == 5: #mayor que
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1>v2)
                    
        elif op == 6: #igual
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1==v2)
        
        elif op == 7: #diferente a
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1!=v2)
         
        elif op == 8: #asignacion
            v1 = lee_memoria(cuad[1])            
            if type(v1) == mem_type(cuad[3]):
                guarda_en_memoria(cuad[3], v1)
            else:
                ad = "- " + str(type(v1)) + ' cannot be assigned to ' + str(mem_type(cuad[3]))
                s_error(0, ad)

        elif op == 9: #and
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            if v1 and v2:
                guarda_en_memoria(cuad[3], True)
            else:
                guarda_en_memoria(cuad[3], False)

        elif op == 10: #or
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            if v1 or v2:
                guarda_en_memoria(cuad[3], True)
            else:
                guarda_en_memoria(cuad[3], False)

        elif op == 11: #not
            v1 = lee_memoria(cuad[1])
            if v1:
                guarda_en_memoria(cuad[3], False)
            else:
                guarda_en_memoria(cuad[3], True)
            
        elif op == 12: # print
            v1 = lee_memoria(cuad[3])
            if type(v1) == type([]):
                print lee_arreglo(v1),
            else:
                print v1
        
        elif op == 13: # gotof
            v1 = lee_memoria(cuad[1])
            if type(v1) == type(True) or type(v1) == type(0):
                if v1 == False or v1 == 0:
                    ieje = int(cuad[3])
            else:
                ad = "- " + str(type(v1)) + " No es valido."
                s_error(2, ad)
        
        elif op == 14: # gotov
            v1 = lee_memoria(cuad[1])
            if type(v1) == type(True) or type(v1) == type(0):
                if v1 == True or v1 != 0:
                    ieje = int(cuad[3])
            else:
                ad = "- " + str(type(v1)) + " No es valido."
                s_error(2, ad)
        
        elif op == 15: # goto
            ieje = int(cuad[3])        
            
        ieje += 1
        
# Guarda la direccion
def guarda_en_memoria(direccion, value):    
    class_memory = memglobal.mem_class(direccion)
    if class_memory == 0:
        memglobal.set(direccion, value)
    elif class_memory == 1:
        memlocal.set(direccion, value)
    elif class_memory == 2:
        memconst.set(direccion, value)
    elif class_memory == 3:
        memtemp.set(direccion, value)
    elif class_memory == 4:
        return memresto.set(direccion, value)
    else:
        print "Error en memoria:", direccions, class_memory
        exit(1)

#Regresa el valor de la direccion
def lee_memoria(direccion):    
    class_memory = memglobal.mem_class(direccion)
    
    if class_memory == 0:
        return memglobal.read(direccion)
    if class_memory == 1:
        return memlocal.read(direccion)
    if class_memory == 2:
        return memconst.read(direccion)
    if class_memory == 3:
        return memtemp.read(direccion)
    if class_memory == 4:
        return memresto.read(direccion)
    else:
        print "Error en lectura:", direccion, class_memory
        exit(1)

# Descripción: Método de instancia el cual nos indica si el registro de memoria de la funcion esta listo.
def registro_listo(self):
    return stackeje.stack.Peek().rm.Ready()

def main():
    cargarArchivo('cod.obj')
    if permiteEjecutar():
        ejecutaCuadruplos()
    print memconst.get()
    print memglobal.get()



if __name__ == "__main__":
    main()
