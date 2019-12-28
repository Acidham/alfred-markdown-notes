#!/usr/bin/python
import os

from Alfred import Items, Plist, Tools


def get_variables():
    config = Plist()
    return config.getConfig()


def print_config():
    variables = get_variables()
    for k, v in variables.items():
        v_subtitle = '<EMPTY>' if v == str() else v
        wf.setItem(
            title=k,
            subtitle='Value: ' + v_subtitle + ' , press SHIFT for Help.',
            arg='selection|%s|%s' % (k, v),
            quicklookurl='file://' + wf_dir + '/docs/' + k + ".md"
        )
        icon = 'icons/check.png' if v != str() else 'icons/question.png'
        wf.setIcon(
            icon,
            'image'
        )
        wf.addItem()


def get_selection(key, query):
    variables = get_variables()
    if key in variables:
        v = variables[key]
        isValid = False if query == str() else True
        wf.setItem(
            title='Change %s: %s' % (key, v),
            subtitle=u'Add new value for "{0}" and press enter. SHIFT for Help, \u2318 to delete value'.format(
                key),
            arg='set|%s|%s' % (key, query),
            valid=isValid,
            quicklookurl='file://' + wf_dir + '/docs/' + key + ".md"
        )
        wf.setIcon(
            'icons/edit.png',
            'image'
        )
        wf.addMod(
            key='cmd',
            subtitle='Delete Value',
            arg='set|{0}|'.format(key)
        )
        wf.addModsToItem()
        wf.addItem()
    else:
        wf.setItem(
            title="variable not found",
            valid=False
        )
        wf.addItem()


def write_config(key, value):
    """
    Writes config item to plist file

    Args:
        key (str): key of key-value pair
        value (str): value of key-value pair
    """
    config = Plist()
    config.setVariable(key, value)
    value = '<EMPTY>' if value == str() else value
    wf.setItem(
        title="Proceed?",
        subtitle='%s will be changed to: %s' % (key, value),
        arg=''
    )
    wf.setIcon(
        'icons/hand.png',
        'image'
    )
    wf.addItem()


action_key_value = Tools.getEnv('action_key_value')
[action, key, value] = action_key_value.split(
    '|') if action_key_value != str() else [str(), str(), str()]
wf_dir = os.getcwd()
query = Tools.getArgv(1)

wf = Items()

if action == str():
    print_config()
elif action == 'selection':
    get_selection(key, query)
else:
    write_config(key, value)

wf.write()
