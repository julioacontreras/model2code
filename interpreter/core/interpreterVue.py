#!/usr/bin/env python
# -*- coding: utf-8 -*-
from interpreter import Interpreter

class InterpreterVue:

    def __init__(self, configJSON):
        self.interpreter = Interpreter(configJSON)
        self.config = self.interpreter.getConfig()
        pass

    def getConfig(self):
        return self.config

    def addImports(self, data):
        code = "\n"
        for c in data['components']:
            code += "import {} from '@/{}/{}'\n".format(c['parameters']['name'], c['parameters']['area'], c['parameters']['filename'])
        return code

    def addComponentOnGlobal(self, data):
        code = "\n"
        for c in data['components']:
            code += "Vue.component('{}','{}');\n".format(c['parameters']['tag'] , c['parameters']['name'])
        return code

    def addComponentOnClass(self, data):
        code = "components:{\n"
        for c in data['components']:
            code += "   {},\n".format(c['parameters']['name'])
        code += "},\n"
        return code

    def addComponentOnTemplate(self, data):
        code = "\n"
        for c in data['components']:
            code += "<{}/>\n".format(c['parameters']['tag'])
        return code

    def generateCode(self, item, model, content):
        if 'actions' in item:
            for el in item['actions']:
                if el['action'] == "addImports":
                    content = self.interpreter.replace(content, el['tag'], self.addImports(model) )
                if el['action'] == "addComponentOnGlobal":
                    print('  adding component on global...')
                    content = self.interpreter.replace(content, el['tag'], self.addComponentOnGlobal(model) )
                if el['action'] == "addComponentOnClass":
                    print('  adding component on class...')
                    content = self.interpreter.replace(content, el['tag'], self.addComponentOnClass(model) )
                if el['action'] == "addComponentOnTemplate":
                    print('  adding component on template...')
                    content = self.interpreter.replace(content, el['tag'], self.addComponentOnTemplate(model) )
        return content

    def generate(self, filenameJSON):
        templateDirectory = self.interpreter.getPathTemplate()
        outputDirectory = self.interpreter.getPathOut()
        model = self.interpreter.loadModel(filenameJSON)
        print('  Name: ' + model['project'])
        print('  description: ' + model['description'])
        print('')
        print('Generation actions Vue: ')
        print('------------------- ')
        for el in self.config['actions']:

            if el['action'] == "restartProject":
                self.interpreter.restartProject()

            if el['action'] == "createDirectory":
                print("- Create directory {} ...".format(el['pathOut']))
                self.interpreter.createDirectory(outputDirectory + el['pathOut'])

            if el['action'] == "copy":
                filenameIn = templateDirectory+"{}/{}".format(el["pathIn"], el['filename'])
                print("- Coping file {} ...".format(filenameIn))
                content = self.interpreter.loadFile(filenameIn)
                content = self.generateCode(el, model, content)
                filenameOut = outputDirectory+"{}/{}".format(el["pathOut"], el['filename'])
                self.interpreter.saveFile(filenameOut, content)
                self.interpreter.verifyFile(filenameOut)

            if el['action'] == "execute":
                cmd = el['command']
                self.interpreter.execute(cmd)
