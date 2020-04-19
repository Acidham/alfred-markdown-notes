#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib

import MyNotes
from Alfred import Items as Items
from Alfred import Tools as Tools

# create MD search object
md_search = MyNotes.Search()

# Load environment variables
ext = md_search.getNotesExtension()
p = md_search.getNotesPath()
query = Tools.getArgv(1)
todos = md_search.todoSearch(query)

wf = Items()
if len(todos) > 0:
    for i in todos:
        md_path = urllib.pathname2url(i['path'])
        md_title = i['title'] if i['title'] != str(
        ) else Tools.chop(i['filename'], ext)
        wf.setItem(
            title=i['todo'],
            subtitle=u'\u2192 {0} (Created: {1})'.format(
                md_title.decode('utf-8'), Tools.getDateStr(i['ctime'])),
            arg=i['path'],
            valid=True,
            type='file'
        )
        wf.setIcon('icons/unchecked.png', 'image')
        # Mod for CMD - new action menu
        wf.addMod(
            key="cmd",
            arg="{0}>{1}".format(i['path'], query),
            subtitle="Actions..",
            icon_path="icons/action.png",
            icon_type="image"
        )
        # TODO: REmove
        # wf.addModsToItem()
        wf.addItem()
else:
    wf.setItem(
        title="No todo found!",
        subtitle="No todo matches search term",
        valid=False
    )
    wf.addItem()
wf.write()
