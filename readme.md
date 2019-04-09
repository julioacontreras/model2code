# Model2Code

Tool to convert model to code.

## Dependencies

* Python 2.7.15

## Execute

python main.py [`projectJSON`] [`modelPath`] [`interpreters`]

`projectJSON`: Filename project in format JSON.

`modelPath`: Pathname project with containg the model files.

`interpreters`: Interpreters you want to use.

~~~
interpreter/$python main.py myproject.json ../input/example interpreterVue:vue.json,interpreterPG:pg.json
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

### Example to create your interpreter

Model:
~~~json
{
    "project": "My Application",
    "description": "My super amazing application",
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

Interpreter config:
~~~json
{
    "root": "/example",
    "inPath": "../../input/example",
    "outPath": "c:/myabsolutepath/model2code/output",
    "templatePath": "../input/example/templates/vue",
    "symbol": "@@",
    "actions" : [
        { "action": "createDirectory", "pathOut":""},
        { "action": "createDirectory", "pathOut":"/front"},
        { "action": "createDirectory", "pathOut":"/front/src"},
        { "action": "copy", "filename": "App.vue", "pathIn":"/src", "pathOut":"/front/src",
            "actions": [
                  {"action": "myFunction", "tag": "my-tag"}
            ]
        }
    ]
}
~~~

Template:
~~~javascript
<template>
    <div/>
</template>

<script>

export default {
      components:{
          @@my-tag@@
      }
}
</script>
~~~

Interpreter:
~~~python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from interpreter import Interpreter

class InterpreterVue:

    def __init__(self, configJSON):
        self.interpreter = Interpreter(configJSON)
        self.config = self.interpreter.getConfig()
        pass

    def myFunction(self, data):
        code = "\n"
        for c in data['components']:
            code += "<{}/>\n".format(c['parameters']['tag'])
        return code

    def generateCode(self, item, model, content):
        if 'actions' in item:
            for el in item['actions']:
                if el['action'] == "myFunction":
                    print('  adding myFunction works!...')
                    content = self.interpreter.replace(content, el['tag'], self.myFunction(model) )
        return content

    def generate(self, filenameJSON):
        templateDirectory = self.interpreter.getPathTemplate()
        outputDirectory = self.interpreter.getPathOut()
        model = self.interpreter.loadModel(filenameJSON)
        for el in self.config['actions']:

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
