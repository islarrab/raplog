# -*- coding: cp1252 -*-
#
# Autores: Melissa M. Gonz�lez Mtz. A01087765
#          Isaac Larraguibel Bours A00231505
#
# Clase: Compiladores
# Profesora: Elda Guadalupe Quiroga Gonz�lez
# Fecha: 21 de Noviembre del 2012
#
# Descripci�n: Programa que enlaza al parser con la maquina virtual
# Valores de entrada : Nada
# Valores de salida : Nada
#

import sys
import os
import mv

def main():
    a="raplog"
    os.system("parser.py "+a)
    os.system("mv.py "+a+".rlo")

if __name__ == "__main__":
    main()
