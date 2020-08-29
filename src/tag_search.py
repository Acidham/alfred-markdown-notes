#!/usr/bin/python3
# -*- coding: utf-8 -*-

from unicodedata import normalize

from Alfred3 import Items as Items
from Alfred3 import Keys as K
from Alfred3 import Tools as Tools
from MyNotes import Search

# create MD search object
md = Search()

# Get environment variables
ext = md.getNotesExtension()
query = normalize('NFC', Tools.getArgv(1))  # Tag name

if query is str():
    # Tag Search and sort based on tag name
    tag_results = md.tagSearch(query, 'tag', reverse=False)
else:
    # Tag Search and sort based on number of Hits
    tag_results = md.tagSearch(query, 'count', reverse=True)

wf = Items()

if bool(tag_results):
    for tag, counter in tag_results.items():
        wf.setItem(
            title=f'{tag}',
            subtitle=f"{counter} Hit(s), ({K.CMD} to paste tag into frontmost app)",
            valid=True,
            arg=f'#{tag}'
        )
        wf.setIcon('icons/hashtag.png', 'image')
        wf.addMod(
            key='cmd',
            arg=f'#{tag} ',
            subtitle='Paste Tag into frontmost app',
            icon_path='icons/paste.png',
            icon_type='image'
        )
        wf.addItem()
else:
    wf.setItem(
        title="No Tags found!",
        subtitle="No Tags matches search term",
        valid=False
    )
    wf.addItem()
wf.write()
