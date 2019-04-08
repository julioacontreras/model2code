#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import shutil

class Interpreter:

    def __init__(self, configJSON):
        self.config = self.loadJSON(configJSON)
        self.symbol = self.config['symbol']
        pass

    def restartProject(self):
        self.removeDirectory( self.getPathOut() )
        self.createDirectory( self.getPathOut() )

    def getConfig(self):
        return self.config

    def getPathOut(self):
        return self.config['outPath'] + self.config['root']

    def getPathTemplate(self):
        return self.config['templatePath']

    def getSymbolInterpreter(self):
        return self.symbol

    def replace(self, content, tag, value):
        return content.replace(self.symbol + tag + self.symbol, value )

    def verifyFile(self, filename):
        if os.path.isfile(filename) == False:
            print("  Error: file not copied!")
        else:
            print("  Copy to {}".format(filename))

    def copyFile(self, templateDirectory, outputDirectory, filename):
        content = self.loadFile(templateDirectory+"/{}".format(filename))
        self.saveFile(outputDirectory+"/{}".format(filename), content)
        self.verifyFile(outputDirectory+"/{}".format(filename))

    def loadFile(self, filepath):
        fIn = open(filepath,"r")
        return fIn.read()

    def saveFile(self, filepath, content):
        fOut = open(filepath,"w")
        fOut.write(content)

    def loadJSON(self, filenameJSON):
        with open(filenameJSON) as json_file:
            data = json.load(json_file)
            return data

    def loadModel(self, filenameJSON):
        return self.loadJSON(filenameJSON)

    def removeDirectory(self, path):
        if os.path.isdir(path):
            print ("Remove directory {}".format(path))
            shutil.rmtree(path)

    def createDirectory(self, path):
        try:
            os.mkdir(path)
        except OSError:
            print ("  Creation of the directory %s failed" % path)
        else:
            print ("  Successfully created the directory %s " % path)

    def execute(self, command):
        command = command.replace("{pathOut}", self.getPathOut())
        print("- Executing command {} ...".format(command))
        os.system(command)
        return command
