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
            subtitle=u'\u2192 %s (Created: %s)' % (
                md_title.decode('utf-8'), Tools.getDateStr(i['ctime'])),
            arg=i['path'],
            valid=True,
            type='file'
        )
        wf.setIcon('icons/unchecked.png', 'image')
        # Mod for CTRL - delete a Note
        wf.addMod(
            key="ctrl",
            arg=Tools.strJoin(i['path'], '|', query),
            subtitle="Delete Note",
            valid=True,
            icon_path="icons/delete.png",
            icon_type="image"
        )
        wf.addModsToItem()
        # Mod for CMD  to copy Markdown Link
        wf.addMod(
            key='cmd',
            arg='[%s](%s)' % (i['filename'], md_path),
            subtitle='Copy Markdown Link to Clipboard',
            valid=True,
            icon_path='icons/link.png',
            icon_type='image'
        )
        wf.addModsToItem()
        # Mod for FN - open in Marked 2
        wf.addMod(
            key='fn',
            arg=i['path'],
            subtitle='Open Preview in Marked 2',
            valid=True,
            icon_path='icons/marked.png',
            icon_type='image'
        )
        wf.addModsToItem()
        wf.addItem()
else:
    wf.setItem(
        title="No todo found!",
        subtitle="No todo matches search term",
        valid=False
    )
    wf.addItem()
wf.write()
