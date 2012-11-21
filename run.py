#!/usr/bin/env python
# -*- coding: cp1252 -*-

import sys
import os
import mv

def main():
    a="raplog"
    os.system("parser.py "+a)
    os.system("mv.py "+a+".rlo")

if __name__ == "__main__":
    main()
