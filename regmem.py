#!/usr/bin/env python
# -*- coding: cp1252 -*-
class RegistroMemoria(object):

    def __init__(self):
        self.tamanosLocales = []
        self.tamanosTemporales = []
        self.offsetsLocales = []
        self.offsetsTemporales = []
        self.direccionRetorno = 0
        self.direccionEjecucion = 0
        self.ready = False
        
    # Descripción: Constructor del objeto Registro Memoria con los 4 arreglos de offses y tamaños, la direccion de retorno, direccion de ejecucion y el boolean ready
    # Entrada: loc, temp, oloc, otem, dirret, direjec, read

    def RegistroMemoria(self, loc, temp, oloc, otem, dirret, direjec, read):
        self.tamanosLocales = loc
        self.tamanosTemporales = temp
        self.offsetsLocales = oloc
        self.offsetsTemporales = otem
        self.direccionRetorno = dirret
        self.direccionEjecucion = direjec
        self.ready = read;

    def getReady(self):
        return self.ready

    def setReady(self, value):
        self.ready = value

    def getEjecucionRetorno(self):
        return self.direccionEjecucion

    def setEjecucionRetorno(self, value):
        self.direccionEjecucion = value

    def getAlmacenRetorno(self):
        return self.direccionRetorno

    def setAlmacenRetorno(self, value):
        self.direccionRetorno = value

    def getTamanoLocal(self):
        return self.tamanosLocales

    def setTamanoLocal(self, value):
        self.tamanosLocales = value

    def getTamanoTemporal(self):
        return self.tamanosTemporales

    def setTamanoTemporal(self, value):
        self.tamanosTemporales = value

    def getOffsetLocal(self):
        return self.offsetsLocales

    def setOffsetLocal(self, value):
        self.offsetsLocales = value

    def getOffsetTemporal(self):
        return self.offsetsTemporales

    def setOffsetTemporal(self, value):
        self.offsetsTemporales = value
