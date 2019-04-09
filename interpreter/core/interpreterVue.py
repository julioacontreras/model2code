#!/usr/bin/env python
# -*- coding: utf-8 -*-
from interpreter import Interpreter

class InterpreterVue:

    def __init__(self, configJSON):
        self.interpreter = Interpreter(configJSON)
        self.config = self.interpreter.getConfig()
        pass

    def addImports(self, data):
        code = ""
        for c in data['components']:
            code += "import {} from '@/{}/{}'\n".format(c['name'], c['parameters']['area'], c['parameters']['filename'])
        return code

    def addComponentInGlobal(self, data):
        code = ""
        for c in data['components']:
            code += "Vue.component('{}','{}');\n".format(c['parameters']['tag'] , c['name'])
        return code

    def addComponentInClass(self, data):
        code = ""
        for c in data['components']:
            s = self.interpreter.getSeparator(",", "", c, data['components'])
            code += "   '{}':{}{}\n".format(c['parameters']['tag'], c['name'], s)
        return code

    def addComponentInTemplate(self, data):
        code = ""
        for c in data['components']:
            code += "<{}/>\n".format(c['parameters']['tag'])
        return code

    def addModelInTemplate(self, elM):
        code = ""
        for m in elM['fields']:
            title = ""
            if 'label' in m['parameters']:
                title = '<label>{}</label>'.format(m['parameters']['label'])
            code += "           {}<{} v-model='{}' type='{}' />\n".format(
                    title,
                    m['parameters']['tagTemplate'],
                    m['field'],
                    m['parameters']['typeElement']
                )
        return code

    def addModelInData(self, elM):
        code = ""
        for m in elM['fields']:
            code += "           '{}':'{}',\n".format(
                    m['field'],
                    m['parameters']['valueDefaultData']
                )
        return code

    def generateCode(self, item, model, content):
        if 'actions' in item:
            for el in item['actions']:
                if el['action'] == "addImports":
                    content = self.interpreter.replace(content, el['tag'], self.addImports(model) )
                if el['action'] == "addComponentInGlobal":
                    print('  adding component in global...')
                    content = self.interpreter.replace(content, el['tag'], self.addComponentInGlobal(model) )
                if el['action'] == "addComponentInClass":
                    print('  adding component in class...')
                    content = self.interpreter.replace(content, el['tag'], self.addComponentInClass(model) )
                if el['action'] == "addComponentInTemplate":
                    print('  adding component in template...')
                    content = self.interpreter.replace(content, el['tag'], self.addComponentInTemplate(model) )
        return content

    def generateCodeViews(self, item, elM, content):
        if 'actions' in item:
            for el in item['actions']:
                if el['action'] == "addModelInTemplate":
                    print('  adding model in template...')
                    content = self.interpreter.replace(content, el['tag'], self.addModelInTemplate(elM) )
                if el['action'] == "addModelInData":
                    print('  adding model in data...')
                    content = self.interpreter.replace(content, el['tag'], self.addModelInData(elM) )
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

            if el['action'] == "copyViews":
                for elM in model['models']:
                    filenameIn = templateDirectory+"{}/{}".format(el["pathIn"], el['filename'])
                    print("- Coping file {} ...".format(filenameIn))
                    content = self.interpreter.loadFile(filenameIn)
                    content = self.generateCodeViews(el, elM, content)
                    filenameOut = outputDirectory+"{}/{}".format(el["pathOut"], elM['name'].capitalize() + ".vue" )
                    self.interpreter.saveFile(filenameOut, content)
                    self.interpreter.verifyFile(filenameOut)

            if el['action'] == "execute":
                cmd = el['command']
                self.interpreter.execute(cmd)
