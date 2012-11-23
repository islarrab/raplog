# -*- coding: cp1252 -*-
#
# Autores: Melissa M. González Mtz. A01087765
#          Isaac Larraguibel Bours A00231505
#
# Clase: Compiladores
# Profesora: Elda Guadalupe Quiroga González
# Fecha: 21 de Noviembre del 2012
#
# Descripción: Es la Maquina virtual que se encarga de leer el archivo .rlo
# generado por el parser y procesar los cuadruplos
# Valores de entrada : Nombre de archivo
# Valores de salida : Ejecucion de los cuadruplos
#

#!/usr/bin/env python

import sys
import os
import time
from mem import *
from fun import *
import shlex
import turtle
import math
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
            

#Descripción: Método de instancia el cual nos indica si es posible o no ejecutar un cuadruplo en la Maquina virtual
def permiteEjecutar():
    if (getTotalCuad() > 0) and (ieje != getTotalCuad()):
        return True
    else:
        return False

#Descripción: Método de instancia el cual ejecuta el siguiente cuadruplo y escribe el objeto MensajeCuadruplo con la información de regreso
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
            #print "left("+str(v1)+")"
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
        
        elif ieje == dir.f_mathpow: #mathpow
            v1 = lee_memoria(arreglotemp.param.pop())
            v2 = lee_memoria(arreglotemp.param.pop())
            guarda_en_memoria(10000, math.pow(v1,v2))
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            a = True
        
        elif ieje == dir.f_begin_fill:
            turtle.begin_fill()
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            a = True
        
        elif ieje == dir.f_end_fill:
            turtle.end_fill()
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            a = True
        
        elif ieje == dir.f_color:
            v1 = lee_memoria(arreglotemp.param.pop())
            v2 = lee_memoria(arreglotemp.param.pop())
            turtle.color(v1, v2)
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            a = True
        
        elif ieje == dir.f_pencolor:
            v1 = lee_memoria(arreglotemp.param.pop())
            v2 = lee_memoria(arreglotemp.param.pop())
            v3 = lee_memoria(arreglotemp.param.pop())
            turtle.pencolor(v1, v2, v3)
            arreglotemp = stack.pop()
            ieje = arreglotemp.ieje
            a = True
        
        elif ieje == dir.f_fillcolor:
            v1 = lee_memoria(arreglotemp.param.pop())
            v2 = lee_memoria(arreglotemp.param.pop())
            v3 = lee_memoria(arreglotemp.param.pop())
            turtle.fillcolor(v1, v2, v3)
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
            
            guarda_en_memoria(cuad[3], v1)
            #if type(v1) == memglobal.tipoMem(cuad[3]):
            #    guarda_en_memoria(cuad[3], v1)
            #else:
            #    print "- " + str(type(v1)) + ' cannot be assigned to ' + str(memglobal.tipoMem(cuad[3]))

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
            sys.stdout.write(str(v1).replace("\\n", "\n"))
        
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
            arreglotemp.valor = v1
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
            turtle.done()
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
    if (len(sys.argv) <= 1):
        print('No file specified, exiting now')
    else:
        turtle.title("Raplog - "+sys.argv[1])
        cargarArchivo(sys.argv[1])
        if permiteEjecutar():
            ejecutaCuadruplos()
            if a:
                exit(1)



if __name__ == "__main__":
    # parametros iniciales de trutle
    turtle.title("Raplog")
    turtle.speed("normal")
    turtle.tracer(True)
    main()
    sys.stdout.close()
