#!/usr/bin/env python
# -*- coding: utf-8 -*-
from interpreter import Interpreter

class InterpreterPG:

    def __init__(self, configJSON):
        self.interpreter = Interpreter(configJSON)
        self.config = self.interpreter.getConfig()
        pass

    def getConfig(self):
        return self.config

    def addName(self, data):
        code = data['name']
        return code

    def addColumns(self, data):
        code = "\n"
        for c in data['fields']:
            code += "{} {},\n".format(c['field'] , c['type'])
        return code

    def generateCode(self, item, model, content):
        if 'actions' in item:
            for el in item['actions']:
                if el['action'] == "addColumns":
                    print('  adding columns...')
                    content = self.interpreter.replace(content, el['tag'], self.addColumns(model) )
                if el['action'] == "addName":
                    print('  adding name...')
                    content = self.interpreter.replace(content, el['tag'], self.addName(model) )
        return content

    def generate(self, filenameJSON):
        templateDirectory = self.interpreter.getPathTemplate()
        outputDirectory = self.interpreter.getPathOut()
        model = self.interpreter.loadModel(filenameJSON)
        print('  Name: ' + model['project'])
        print('  description: ' + model['description'])
        print('')
        print('Generation actions Postgres: ')
        print('--------------------------- ')
        for el in self.config['actions']:

            if el['action'] == "restartProject":
                self.interpreter.restartProject()

            if el['action'] == "createDirectory":
                print("- Create directory {} ...".format(el['pathOut']))
                self.interpreter.createDirectory(outputDirectory + el['pathOut'])

            if el['action'] == "copyTables":
                for elM in model['models']:
                    filenameIn = templateDirectory+"{}/{}".format(el["pathIn"], el['filename'])
                    print("- Coping file {} ...".format(filenameIn))
                    content = self.interpreter.loadFile(filenameIn)
                    content = self.generateCode(el, elM, content)
                    filenameOut = outputDirectory+"{}/{}".format(el["pathOut"], elM['name'] + ".sql")
                    self.interpreter.saveFile(filenameOut, content)
                    self.interpreter.verifyFile(filenameOut)

            if el['action'] == "execute":
                cmd = el['command']
                self.interpreter.execute(cmd)
