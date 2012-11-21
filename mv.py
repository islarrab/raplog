#!/usr/bin/env python
# -*- coding: cp1252 -*-

import sys
import os
from mem import *
from fun import *
import shlex
import turtle
import dir

memglobal = Memoria(0)
memconst = Memoria(80000)
memresto = Memoria(200000)
arreglotemp = Funciones()
cuadruplos = []
ieje = 0
param = []
stack = []
a = False

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
            

#Descripci�n: M�todo de instancia el cual nos indica si es posible o no ejecutar un cuadruplo en la Maquina virtual
def permiteEjecutar():
    if (getTotalCuad() > 0) and (ieje != getTotalCuad()):
        return True
    else:
        return False

#Descripci�n: M�todo de instancia el cual ejecuta el siguiente cuadruplo y escribe el objeto MensajeCuadruplo con la informaci�n de regreso
#Entrada: cuad
def ejecutaCuadruplos():
    global ieje, arreglotemp, a
    while ieje < getTotalCuad():
        if ieje == dir.f_forward: #forward
            v1 = lee_memoria(arreglotemp.param.pop())
            turtle.forward(v1)
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            a = True

        elif ieje == dir.f_backward: #backward
            v1 = lee_memoria(arreglotemp.param.pop())
            turtle.backward(v1)
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            a = True
            
        elif ieje == dir.f_right: #right
            v1 = lee_memoria(arreglotemp.param.pop())
            turtle.right(v1)
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            a = True
            
        elif ieje == dir.f_left: #left
            v1 = lee_memoria(arreglotemp.param.pop())
            turtle.left(v1)
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            a = True

        elif ieje == dir.f_goto: #turtle_goto
            v1 = lee_memoria(arreglotemp.param.pop())
            v2 = lee_memoria(arreglotemp.param.pop())
            turtle.goto(v1,v2)
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            a = True
            
        elif ieje == dir.f_setx: #setx
            v1 = lee_memoria(arreglotemp.param.pop())
            turtle.setx(v1)
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            a = True
            
        elif ieje == dir.f_sety: #sety
            v1 = lee_memoria(arreglotemp.param.pop())
            turtle.sety(v1)
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            a = True

        elif ieje == dir.f_speed: #speed
            v1 = lee_memoria(arreglotemp.param.pop())
            turtle.speed(v1)
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            a = True

        elif ieje == dir.f_position: #position
            v1 = turtle.position()
            arreglotemp.valor = v1
            a = True

        elif ieje == dir.f_towards: #towards
            v1 = lee_memoria(arreglotemp.param.pop())
            v2 = lee_memoria(arreglotemp.param.pop())
            turtle.towards(v1,v2)
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            a = True
            

        cuad= cuadruplos[ieje]
        ieje +=1
        
        op= cuad[0]
        if(cuad[1]>=160000):
            cuad[1]=lee_memoria(cuad[1])
        if(cuad[2]>=160000):
            cuad[2]=lee_memoria(cuad[2])
        
        if op == dir.suma: # suma
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1+v2)

        elif op == dir.resta: #resta
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1-v2)
            
        elif op == dir.multi: #multiplicacion
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1*v2)
            
        elif op == dir.div: #division
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1/v2)
            
        elif op == dir.menorq: #menor que
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1<v2)

        elif op == dir.mayorq: #mayor que
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1>v2)
                    
        elif op == dir.igual: #igual
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1==v2)
        
        elif op == dir.difer: #diferente a
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1!=v2)
         
        elif op == dir.asigna: #asignacion
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

        elif op == dir.andd: #and
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            if v1 and v2:
                guarda_en_memoria(cuad[3], True)
            else:
                guarda_en_memoria(cuad[3], False)

        elif op == dir.orr: #or
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            if v1 or v2:
                guarda_en_memoria(cuad[3], True)
            else:
                guarda_en_memoria(cuad[3], False)

        elif op == dir.nott: #not
            v1 = lee_memoria(cuad[1])
            if v1:
                guarda_en_memoria(cuad[3], False)
            else:
                guarda_en_memoria(cuad[3], True)
            
        elif op == dir.printt: # print
            v1 = lee_memoria(cuad[1])
            if type(v1) == type([]):
                print lee_arreglo(v1)
            else:
                print v1
        
        elif op == dir.gotof: # gotof
            v1 = lee_memoria(cuad[1])
            if type(v1) == bool or type(v1) == int:
                if v1 == False or v1 == 0:
                    ieje = int(cuad[3])
            else:
                print "* " + str(type(v1)) + " No es valido."
        
        elif op == dir.gotov: # gotov
            v1 = lee_memoria(cuad[1])
            if type(v1) == bool or type(v1) == int:
                if v1 == True or v1 != 0:
                    ieje = int(cuad[3])
            else:
                print "* " + str(type(v1)) + " No es valido."        
        elif op == dir.goto: # goto
            ieje = int(cuad[3])

        elif op == dir.menorigualq: #menorigual que
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1<=v2)

        elif op == dir.mayorigualq: #mayorigual que
            v1 = lee_memoria(cuad[1])
            v2 = lee_memoria(cuad[2])
            guarda_en_memoria(cuad[3], v1>=v2)

        elif op == dir.era: #era
            arrFun = Funciones()
        
        elif op == dir.gosub: # gosub
            arreglotemp.ieje = ieje
            stack.append(arreglotemp)
            ieje = cuad[1]
            arreglotemp = arrFun
        
        elif op == dir.ret: # ret
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            
        elif op == dir.param: # param
            v1 = lee_memoria(cuad[1])
            direccionP = cuad[3]
            arrFun.setParam(direccionP, v1, arreglotemp, memresto)

        elif op == dir.retorno: # return
            tipoRetorno = memglobal.tipoMem(cuad[1])
            v1 = lee_memoria(cuad[1])
            arreglotemp = stack.pop()
        
            if tipoRetorno == type(v1):
                arreglotemp.valor = v1
            else:
                print "* " + str(type(v1)) + "no es un tipo correcto, se espera el tipo", tipoRetorno, "."   
            ieje = arreglotemp.ieje
            
        elif op == dir.scan: #scan
            v1 = memglobal.tipoMem(cuad[3])(raw_input("-"))
            if type(v1) == memglobal.tipoMem(cuad[3]):
                guarda_en_memoria(cuad[3], v1)
            else:
                print "* " + str(type(v1)) + ' no se puede asignar con un ' + str(memglobal.tipoMem(cuad[3]))    

        elif op == dir.verifica: #verifica
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

# Descripci�n: M�todo de instancia el cual nos indica si el registro de memoria de la funcion esta listo.
def registro_listo(self):
    return stackeje.stack.Peek().rm.ready()

def main():
    cargarArchivo('prueba3.rlo')
    if permiteEjecutar():
        ejecutaCuadruplos()
        if a:
            turtle.done()
    #print memconst.get()
    #print memglobal.get()



if __name__ == "__main__":
    main()
