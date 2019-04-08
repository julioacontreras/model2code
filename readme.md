# Model2Code

Tool to convert model to code.

## Dependencies

* Python 2.7.15

## Execute

~~~
interpreter/python main.py
~~~

## Why

* Design more and program less: Most projects have a lot of similar code. This tool allows you to create templates and models to generate code. Increasing productivity and reducing human error.

* Facilitating technology migration: Once you have templates and templates, you can change the technology by changing the interpreter.

* Flexible: If you can choose which parts of your project are generic or not.

## How works

This is the architecture divided into inputs, interpreters and outputs.

* Inputs: All the information that the interpreter needs to generate code containing: template, template and config.

* Interpreters: Are set of actions generate code.

* Outputs: And all the code generated by the interpreters.

~~~
+------------+   +--------------+   +--------------+
| INPUTS     +-->+ INTERPRETERS +-->+ OUTPUTS      |
|            |   |              |   |              |
| - Modelo   |   | - Tech Foo   |   | - MyProject  |
| - Template |   | - Tech Bar   |   |              |
| - Config   |   |              |   |              |
+------------+   +--------------+   +--------------+
~~~

### Model example

~~~json
{
    "project": "My Application",
    "description": "My super amazing application",
    "symbol": "@@",
    "components": [
        {
            "name": "MyForm",
            "parameters":{
                "area": "components",
                "filename": "myForm.vue",
                "tag": "my-form"
            }
        }
    ],
    "models": [
        {
            "name": "user",
            "fields": [
                {"field": "id", "type": "number"},
                {"field": "name", "type": "string"},
                {"field": "age", "type": "integer"},
                {"field": "password", "type": "string"}
            ]
        }
    ]
}
~~~

### Interpreter config example

~~~json
{
    "root": "/example",
    "inPath": "../../input/example",
    "outPath": "c:/myabsolutepath/model2code/output",
    "templatePath": "../input/example/templates/vue",
    "symbol": "@@",
    "actions" : [
        { "action": "restartProject-" },
        { "action": "createDirectory", "pathOut":""},
        { "action": "createDirectory", "pathOut":"/front"},
        { "action": "copy", "filename": "babel.config.js", "pathIn":"", "pathOut":"/front"},
        { "action": "copy", "filename": "package-lock.json", "pathIn":"", "pathOut":"/front"},
        { "action": "copy", "filename": "package.json", "pathIn":"", "pathOut":"/front"},
        { "action": "copy", "filename": "yarn.lock", "pathIn":"", "pathOut":"/front"},
        { "action": "createDirectory", "pathOut":"/front/src"},
        { "action": "copy", "filename": "main.js", "pathIn":"/src", "pathOut":"/front/src",
                  "actions": [
                        {"action": "addImports", "tag": "add-imports"},
                        {"action": "addComponentOnGlobal", "tag": "add-component-on-global"}
                  ]
        },
        { "action": "copy", "filename": "App.vue", "pathIn":"/src", "pathOut":"/front/src",
            "actions": [
                  {"action": "addComponentOnClass", "tag": "add-component-on-class"},
                  {"action": "addComponentOnTemplate", "tag": "add-component-on-template"}
            ]
        },
        { "action": "createDirectory", "pathOut":"/front/src/components"},
        { "action": "copy", "filename": "myForm.vue", "pathIn":"/src/components", "pathOut":"/front/src/components"}
    ]
}
~~~

### Template code example

~~~javascript
<template>
    @@add-component-on-template@@
</template>

<script>

export default {
      components:{
          @@add-component-on-class@@
      }
}
</script>
~~~

### Interpreter example

~~~python
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
        code = ""
        for c in data['components']:
            code += "   {},\n".format(c['parameters']['name'])
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
~~~
