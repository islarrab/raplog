#!/usr/bin/env python
# -*- coding: cp1252 -*-

import mv
import cuadruplos

mi =mv.MV()
mi.MaqVir('prueba1.rlo')
if mi.permiteEjecutar():
    cuad = mi.getCuadruplo()
    mi.ejecutaCuadruplo(cuad, 0)
