#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib.request import pathname2url

import MyNotes
from Alfred3 import Items as Items
from Alfred3 import Keys as K
from Alfred3 import Tools as Tools

# create MD search object
md_search = MyNotes.Search()

# Load environment variables
ext = md_search.getNotesExtension()
query = Tools.getArgv(1)  # Search term

todos = md_search.todoSearch(query)

wf = Items()
if len(todos) > 0:
    for i in todos:
        md_path = pathname2url(i['path'])
        md_title = i['title'] if i['title'] != str() else Tools.chop(i['filename'], ext)
        wf.setItem(
            title=i['todo'],
            subtitle=f"{K.ARROW_RIGHT} {md_title} (Created: {Tools.getDateStr(i['ctime'])}, Modified: {Tools.getDateStr(i['mtime'])})",
            arg=i['path'],
            valid=True,
            type='file'
        )
        wf.setIcon('icons/unchecked.png', 'image')
        # Mod for CMD - new action menu
        wf.addMod(
            key="cmd",
            arg=f"{i['path']}>{query}",
            subtitle="Actions..",
            icon_path="icons/action.png",
            icon_type="image"
        )
        wf.addItem()
else:
    wf.setItem(
        title="No todo found!",
        subtitle="No todo matches search term",
        valid=False
    )
    wf.addItem()
wf.write()
