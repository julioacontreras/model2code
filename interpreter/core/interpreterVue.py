#!/usr/bin/env python
# -*- coding: utf-8 -*-
from interpreter import Interpreter
from plugins.vue.museUI import MuseUI

class InterpreterVue:

    def __init__(self, configJSON):
        self.interpreter = Interpreter(configJSON)
        self.config = self.interpreter.getConfig()
        self.pluginTemplate = MuseUI(self.interpreter)
        pass

    def addImports(self, data):
        code = ""
        for c in data['components']:
            s = self.interpreter.getSeparator(",\n", "", c, data['components'])
            code += "import %(class)s from '@/%(area)s/%(filename)s'%(sep)s" % {
                'class'    : c['name'],
                'area'     : c['parameters']['area'],
                'filename' : c['parameters']['filename'],
                'sep'      : s
            }
        return code

    def addComponentInGlobal(self, data):
        code = ""
        for c in data['components']:
            s = self.interpreter.getSeparator(",\n", "", c, data['components'])
            code += "Vue.component('{}','{}');{}".format(c['parameters']['tag'] , c['name'], s)
        return code

    def addComponentInClass(self, data):
        code = ""
        for c in data['components']:
            s = self.interpreter.getSeparator(",\n", "", c, data['components'])
            code += "        '{}':{}{}".format(c['parameters']['tag'], c['name'], s)
        return code

    def addComponentInTemplate(self, data):
        code = ""
        for c in data['components']:
            s = self.interpreter.getSeparator("\n", "", c, data['components'])
            code += "        <{}/>{}".format(c['parameters']['tag'], s)
        return code

    def addModelInData(self, elM):
        code = ""
        for m in elM['fields']:
            s = self.interpreter.getSeparator(",\n", "", m, elM['fields'])
            code += "           '{}':'{}'{}".format(
                    m['field'],
                    m['parameters']['valueDefaultData'],
                    s
                )
        return code

    def generateCode(self, config, model, content):
        if 'actions' in config:
            for el in config['actions']:
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
                if el['action'] == "addModelInData":
                    print('  adding model in data...')
                    content = self.interpreter.replace(content, el['tag'], self.addModelInData(model) )
            content = self.pluginTemplate.generateCode(config, model, content);

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

            if el['action'] == "copyModels":
                for elM in model['models']:
                    filenameIn = templateDirectory+"{}/{}".format(el["pathIn"], el['filename'])
                    print("- Coping file {} ...".format(filenameIn))
                    content = self.interpreter.loadFile(filenameIn)
                    content = self.generateCode(el, elM, content)
                    filenameOut = outputDirectory+"{}/{}".format(el["pathOut"], elM['name'].capitalize() + ".vue" )
                    self.interpreter.saveFile(filenameOut, content)
                    self.interpreter.verifyFile(filenameOut)

            if el['action'] == "execute":
                cmd = el['command']
                self.interpreter.execute(cmd)
