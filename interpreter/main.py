#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

if __name__ == '__main__':
    print("Code generator")
    print("=======================")

    if len(sys.argv) != 4:
        print("python main.py [project] [path] [interpreterFoo:foo.json,interpreterBar:bar.json,...]")
        sys.exit(0)

    project = sys.argv[1]
    path = sys.argv[2]+"/{}"
    interpreters = sys.argv[3].split(",")

    print("project: {}".format(project))
    print("path: {}".format(path))
    print("interpreters: {}".format(interpreters))

    def fcUppcase(value):
        return value[0].upper()+value[1:]

    for el in interpreters:
        params = el.split(":")
        interpreter = "core.{}".format(params[0])
        config = params[1]
        print("interpreter: {}".format(interpreter))
        InterpreterEntity = __import__(interpreter)
        InterpreterClass = getattr(InterpreterEntity, fcUppcase(params[0]) )
        obj = InterpreterClass(path.format(config))
        obj.generate(path.format(project))
