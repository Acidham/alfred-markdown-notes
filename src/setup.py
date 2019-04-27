#!/usr/bin/python
import os

import Alfred
from Alfred import Tools as Tools
from Alfred import Plist as Plist


action_key_value = Tools.getEnv('action_key_value')
[action, key, value] = action_key_value.split('|') if action_key_value != str() else [str(),str(),str()]
wf_dir = os.getcwd()
query = Tools.getArgv(1)
config = Plist()
variables = config.getConfig()

wf = Alfred.Items()
if action == str():
    for k, v in variables.items():
        wf.setItem(
            title=k,
            subtitle='Value: ' + v + ' , press Shift for Help.',
            arg='selection|%s|%s' % (k, v),
            quicklookurl='file://' + wf_dir + '/docs/' + k + ".md"
        )
        icon = 'icons/check.png' if v != str() else 'icons/question.png'
        wf.setIcon(
            icon,
            'image'
        )
        wf.addItem()
elif action == 'selection':
    if key in variables:
        v = variables[key]
        isValid = False if query == str() else True
        wf.setItem(
            title='Change %s: %s' % (key,v),
            subtitle='Add new value for %s and press enter. Press Shift for Help.' % key,
            arg='set|%s|%s' % (key,query),
            valid=isValid,
            quicklookurl='file://' + wf_dir + '/docs/' + key + ".md"
        )
        wf.setIcon(
            'icons/edit.png',
            'image'
        )
        wf.addItem()
    else:
        wf.setItem(
            title="variable not found",
            valid=False
        )
        wf.addItem()
else:
    config.setVariable(key, value)
    wf.setItem(
        title="Proceed?",
        subtitle='%s changed to: %s' % (key, value),
        arg=''
    )
    wf.setIcon(
        'icons/hand.png',
        'image'
    )
    wf.addItem()
wf.write()
