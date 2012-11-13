#!/usr/bin/env python
# -*- coding: cp1252 -*-

class Procedimiento(object):
        
         #Descripción: Constructor del objeto Procedimiento que nos indica el nombre de una funcion, tipo, direccion de inicio y cuantos slots de memoria de cada tipo son usados
         #Entrada: nombre, tipo, dirInicial, tamanoIntL, tamanoFloatL, tamanoStrL, tamanoBoolL,  tamanoIntT,  tamanoFloatT, tamanoStrT, tamanoBoolT

    def __init__(self):
         self.nombre = None
         self.tipo = None
         self.dirInicial = None
         self.tamanoIntL = None
         self.tamanoFloatL = None
         self.tamanoStrL = None
         self.tamanoBoolL = None
         self.tamanoIntT = None
         self.tamanoFloatT = None
         self.tamanoStrT = None
         self.tamanoBoolT = None
         
    def Procedimiento(self, nombre, tipo, dirInicial, tamanoIntL, tamanoFloatL, tamanoStrL, tamanoBoolL,  tamanoIntT,  tamanoFloatT, tamanoStrT, tamanoBoolT):
        self.nombre = nombre
        self.tipo = tipo
        self.dir_inicial = dir_inicial
        self.tamanoIntL = tamanoIntL
        self.tamanoFloatL = tamanoFloatL
        self.tamanoStrL = tamanoStrL
        self.tamanoBoolL = tamanoBoolL
        self.tamanoIntT = tamanoIntT
        self.tamanoFloatT = tamanoFloatT
        self.tamanoStrT = tamanoStrT
        self.tamanoBoolT = tamanoBoolT
        
    def TamanosLocales(self):
        return [self.tamanoIntL, self.tamanoFloatL, self.tamanoStrL, self.tamanoBoolL]

    def TamanosTemporales(self):
        return [self.tamanoIntT, self.tamanoFloatT, self.tamanoStrT, self.tamanoBoolT]

    def getNombre(self):
        return self.nombre
    
    def setNombre(self, value):
        self.nombre = value
        
    def getTipo(self):
        return self.tipo
    
    def setTipo(self, value):
        self.tipo = value
        
    def getDireccionInicial(self):
        return self.dirinicial
    
    def setDireccionInicial(self, value):
        self.dirinicial = value
            
    def getTamanoIntLocal(self):
        return self.tamanoIntL
    
    def setTamanoIntLocal(self, value):
        self.tamanoIntL = value
        
    def getTamanoFloatLocal(self):
        return self.tamanoFloatL

    def setTamanoFloatLocal(self, value):
        self.tamanoFloatL = value
        
    def getTamanoStrLocal(self):
        return self.tamanoStrL

    def setTamanoStrLocal(self, value):
        self.tamanoStrL = value
        
    def getTamanoBoolLocal(self):
        return self.tamanoBoolL
    
    def setTamanoBoolLocal(self, value):
        self.tamanoBoolL = value
        
    def getTamanoIntTemporal(self):
        return self.tamanoIntT
    
    def setTamanoIntTemporal(self, value):
        self.tamanoIntT = value
        
    def getTamanoFloatTemporal(self):
        return tamanoFloatT
    
    def setTamanoFloatTemporal(self, value):
        self.tamanoFloatT = value

    def getTamanoStrTemporal(self):
        return tamanoStrT
    
    def setTamanoStrTemporal(self, value):
        self.tamanoStrT = value
        
    def getTamanoBoolTemporal(self):
        return tamanoBoolT
    
    def setTamanoBoolTemporal(self, value):
        self.tamanoBoolT = value;
