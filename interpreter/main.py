#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core import InterpreterVue
from core import InterpreterPG

if __name__ == '__main__':
    print("Code generatior v:0.1.0")
    print("=======================")
    path = "../input/example/{}"
    vueG = InterpreterVue( path.format("vue.json") )
    vueG.generate( path.format("myproject.json") );
    pgG = InterpreterPG( path.format("pg.json") )
    pgG.generate( path.format("myproject.json") );
