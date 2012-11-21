# -*- coding: cp1252 -*-
#
# Autores: Melissa M. González Mtz. A01087765
#          Isaac Larraguibel Bours A00231505
#
# Clase: Compiladores
# Profesora: Elda Guadalupe Quiroga González
# Fecha: 21 de Noviembre del 2012
#
# Descripción: Este es un archivo que tiene definidas las variables y sus valores 
# para uso tanto del parser como de la maquina virtual
# Valores de entrada : Nada
# Valores de salida : todas las variables
#

globint = 0
globfloat = 10000
globstr = 20000
globbool = 30000
localint = 40000
localfloat = 50000
localstr = 60000
localbool = 70000
constint = 80000
constfloat = 90000
conststr = 100000
constbool = 110000
tempint = 120000
tempfloat = 130000
tempstr = 140000
tempbool = 150000
pointer = 160000
resto = 200000

suma = 0
resta = 1
multi= 2
div = 3
menorq = 4
mayorq = 5
igual = 6
difer = 7
asigna = 8
andd = 9
orr  = 10
nott = 11
printt = 12
gotof = 13
gotov = 14
goto = 15
menorigualq = 16
mayorigualq = 17
era = 18
gosub = 19
ret = 20
param = 21
retorno = 22
scan = 23
verifica = 24

# funciones pre-definidas
f_forward = -1
f_backward = -2
f_right = -3
f_left = -4
f_goto = -5
f_setx = -6
f_sety = -7
f_speed = -8

f_position = -9
f_towards = -10


of = {
'+':suma,
'-':resta,
'*':multi,
'/':div,
'=':asigna,
'==':igual,
'<>':difer,
'<':menorq,
'>':mayorq,
'<=':menorigualq,
'>=':mayorigualq,
'and':andd,
'or':orr,
'not':nott,
}

