#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MuseUI:

    def __init__(self, interpreter):
        self.interpreter = interpreter
        pass

    def addInitFramework(self):
        return '''import MuseUI from 'muse-ui';
import 'muse-ui/dist/muse-ui.css';
Vue.use(MuseUI)'''

    def _getTag(self, type):
        tag = 'mu-date-input'
        if 'select' in type:
            tag = 'mu-select'
        return tag

    def addModelInTemplate(self, elM):
        code = "<mu-container>\n"
        code += "    <mu-row gutter>\n"
        for m in elM['fields']:
            placeholder = ""
            if 'label' in m['parameters']:
                placeholder = "placeholder='{}'".format(m['parameters']['label'])

            tag = self._getTag(m['parameters']['tagTemplate'])

            #s = self.interpreter.getSeparator("\n", "", m, elM['fields'])

            code += '           <mu-col span="12" lg="12" sm="12">\n'
            code += "           <%(tag)s v-model='%(field)s' type='%(type)s' %(placeholder)s  />\n" % {

                    "placeholder": placeholder,
                    "tag": tag,
                    "field": m['field'],
                    "type": m['parameters']['typeElement']
                }
            code += '           </mu-col>\n'

        code += "    </mu-row>\n"
        code += "</mu-container>\n"
        return code

    def generateCode(self, item, elM, content):
        if 'actions' in item:
            for el in item['actions']:
                if el['action'] == "addModelInTemplate":
                    print('  adding model in template...')
                    content = self.interpreter.replace(content, el['tag'], self.addModelInTemplate(elM) )
                if el['action'] == "addInitFramework":
                    print('  adding initialize framework...')
                    content = self.interpreter.replace(content, el['tag'], self.addInitFramework() )
        return content
