#!/usr/bin/python3
import os

from Alfred3 import Items, Plist, Tools
from Alfred3 import Keys as K


def get_variables():
    config = Plist()
    return config.getConfig()


def print_config(q):
    variables = get_variables()
    for k, v in variables.items():
        if q == str() or q in k:
            v_subtitle = '<EMPTY>' if v == str() else v
            wf.setItem(
                title=k,
                subtitle=f'Value: {v_subtitle} , \u21E7 for Help.',
                arg='selection|%s|%s' % (k, v),
                quicklookurl=f"file://{wf_dir}/docs/{k}.md"
            )
            icon = 'icons/check.png' if v != str() else 'icons/question.png'
            wf.setIcon(
                icon,
                'image'
            )
            wf.addItem()


def get_selection(key, query: str):
    variables = get_variables()
    if key in variables:
        v = variables[key]
        isValid = False if query == str() else True
        wf.setItem(
            title=f'Change {key}: {v}',
            subtitle=f'Add new value for "{key}" and press enter. {K.SHIFT} for Help, {K.CMD} to delete value',
            arg='set|%s|%s' % (key, query),
            valid=isValid,
            quicklookurl=f"file://{wf_dir}/docs/{key}.md"
        )
        wf.setIcon(
            'icons/edit.png',
            'image'
        )
        wf.addMod(
            key='cmd',
            subtitle='Delete Value',
            arg=f'set|{key}|'
        )
        wf.addModsToItem()
        wf.addItem()
    else:
        wf.setItem(
            title="variable not found",
            valid=False
        )
        wf.addItem()


def write_config(key, value: str):
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
        subtitle=f'{key} will be changed to: {value}',
        arg=''
    )
    wf.setIcon(
        'icons/hand.png',
        'image'
    )
    wf.addItem()


query = Tools.getArgv(1)
action_key_value = Tools.getEnv('action_key_value')
[action, key, value] = action_key_value.split('|') if action_key_value != str() else [str(), str(), str()]
wf_dir = os.getcwd()
query = Tools.getArgv(1)

wf = Items()

if action == str():
    print_config(query)
elif action == 'selection':
    get_selection(key, query)
else:
    write_config(key, value)
wf.write()
