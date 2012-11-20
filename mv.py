#!/usr/bin/env python
# -*- coding: cp1252 -*-

import sys
import os
from mem import *
from fun import *
import shlex
import turtle

memglobal = Memoria(0)
memconst = Memoria(80000)
memresto = Memoria(200000)
arreglotemp = Funciones()
cuadruplos = []
ieje = 0
param = []
stack = []

def getIndiceEjecucion():
    return ieje

def getTotalCuad():
    return len(cuadruplos)

def getCuadruplo():
    return cuadruplos[ieje]

def cargarArchivo(fileName):
        ieje = 0

        #Lectura del Archivo del codigo Objeto
        f = open(fileName, "r")        
        #Primera linea
        linea = f.readline()        
        #Lectura de memoria
        while(linea != '---\n'):
            #Lectura de constantes
            c = shlex.split(linea)
            #checando tipo de la constante
            t = memglobal.tipoMem(int(c[0]))
            guarda_en_memoria(int(c[0]),t(c[1]))
            linea = f.readline()
        #Lectura de cuadruplos
        linea = f.readline()
        while True:
            if not linea: break
            c = [int(n) for n in linea.split()]
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
    global ieje, arreglotemp
    while ieje < getTotalCuad():
        if ieje == -1: #forward
            v1 = lee_memoria(arreglotemp.param.pop())
            turtle.forward(v1)
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            
        elif ieje == -2: #right
            v1 = lee_memoria(arreglotemp.param.pop())
            turtle.right(v1)
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            
        elif ieje == -3: #left
            v1 = lee_memoria(arreglotemp.param.pop())
            turtle.left(v1)
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje

        cuad= cuadruplos[ieje]
        ieje +=1
        
        op= cuad[0]
        if(cuad[1]>=160000):
            cuad[1]=lee_memoria(cuad[1])
        if(cuad[2]>=160000):
            cuad[2]=lee_memoria(cuad[2])
        
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
            if cuad[3]>=160000:
                cuad[3]=lee_memoria(cuad[3])            
            if arreglotemp.valor != 0 or arreglotemp.valor:
                v1 = arreglotemp.valor
                arreglotemp.valor = 0
            else:
                v1 = lee_memoria(cuad[1])
            if type(v1) == memglobal.tipoMem(cuad[3]):
                guarda_en_memoria(cuad[3], v1)
            else:
                print "- " + str(type(v1)) + ' cannot be assigned to ' + str(memglobal.tipoMem(cuad[3]))

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
            v1 = lee_memoria(cuad[1])
            if type(v1) == type([]):
                print lee_arreglo(v1)
            else:
                print v1
        
        elif op == 13: # gotof
            v1 = lee_memoria(cuad[1])
            if type(v1) == bool or type(v1) == int:
                if v1 == False or v1 == 0:
                    ieje = int(cuad[3])
            else:
                print "* " + str(type(v1)) + " No es valido."
        
        elif op == 14: # gotov
            v1 = lee_memoria(cuad[1])
            if type(v1) == bool or type(v1) == int:
                if v1 == True or v1 != 0:
                    ieje = int(cuad[3])
            else:
                print "* " + str(type(v1)) + " No es valido."        
        elif op == 15: # goto
            ieje = int(cuad[3])

        elif op == 16: #menorigual que
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1<=v2)

        elif op == 17: #mayorigual que
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1>=v2)

        elif op == 18: #era
            arrFun = Funciones()
        
        elif op == 19: # gosub
            arreglotemp.ieje = ieje
            stack.append(arreglotemp)
            ieje = cuad[1]
            arreglotemp = arrFun
        
        elif op == 20: # ret
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            
        elif op == 21: # param
            v1 = lee_memoria(cuad[1])
            direccionP = cuad[3]
            arrFun.setParam(direccionP, v1, arreglotemp, memresto)

        elif op == 22: # return
            tipoRetorno = memglobal.tipoMem(cuad[1])
            v1 = lee_memoria(cuad[1])
            arreglotemp = stack.pop()
        
            if tipoRetorno == type(v1):
                arreglotemp.valor = v1
            else:
                print "* " + str(type(v1)) + "no es un tipo correcto, se espera el tipo", tipoRetorno, "."   
            ieje = arreglotemp.ieje
            
        elif op == 23: #scan
            v1 = memglobal.tipoMem(cuad[3])(raw_input("-"))
            if type(v1) == memglobal.tipoMem(cuad[3]):
                guarda_en_memoria(cuad[3], v1)
            else:
                print "* " + str(type(v1)) + ' no se puede asignar con un ' + str(memglobal.tipoMem(cuad[3]))    

        elif op == 24: #verifica
            v1 = lee_memoria(cuad[1])
            li = cuad[2]
            ls = cuad[3]
            if not(v1 >= li and v1 <= ls):
                print "* " + str(v1) + ' No esta dentro del limite ' + str(li) + ' - ' + str(ls)

        elif op == -1: #termina el programa
            break;
        
# Guarda la direccion
def guarda_en_memoria(direccion, valor):    
    class_memory = memglobal.claseMem(direccion)
    if class_memory == 0:
        memglobal.set(direccion, valor)
    elif class_memory == 1:
        arreglotemp.memlocal.set(direccion, valor)
    elif class_memory == 2:
        memconst.set(direccion, valor)
    elif class_memory == 3:
        arreglotemp.memtemp.set(direccion, valor)
    elif class_memory == 4:
        return memresto.set(direccion, valor)
    else:
        print "Error en memoria:", direccions, class_memory
        exit(1)

#Regresa el valor de la direccion
def lee_memoria(direccion):    
    class_memory = memglobal.claseMem(direccion)
    
    if class_memory == 0:
        return memglobal.lee(direccion)
    if class_memory == 1:
        return arreglotemp.memlocal.lee(direccion)
    if class_memory == 2:
        return memconst.lee(direccion)
    if class_memory == 3:
        return arreglotemp.memtemp.lee(direccion)
    if class_memory == 4:
        return memresto.lee(direccion)
    else:
        print "Error en lectura:", direccion, class_memory
        exit(1)

# Descripción: Método de instancia el cual nos indica si el registro de memoria de la funcion esta listo.
def registro_listo(self):
    return stackeje.stack.Peek().rm.ready()

def main():
    cargarArchivo('prueba3.rlo')
    if permiteEjecutar():
        ejecutaCuadruplos()
        turtle.done()
    #print memconst.get()
    #print memglobal.get()



if __name__ == "__main__":
    main()
