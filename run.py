# -*- coding: cp1252 -*-
#
# Autores: Melissa M. González Mtz. A01087765
#          Isaac Larraguibel Bours A00231505
#
# Clase: Compiladores
# Profesora: Elda Guadalupe Quiroga González
# Fecha: 21 de Noviembre del 2012
#
# Descripción: Programa que enlaza al parser con la maquina virtual
# Valores de entrada : Nada
# Valores de salida : Nada
#

import sys
import os
import mv

if __name__ == "__main__":
    raplog_file = sys.argv[1]
    os.system("python parser.py "+raplog_file)
    os.system("python mv.py "+raplog_file+".rlo")
