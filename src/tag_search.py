#!/usr/bin/python
# -*- coding: utf-8 -*-

from Alfred import Items as Items
from Alfred import Tools as Tools
from MyNotes import Search

# create MD search object
md = Search()

# Get environment variables
ext = md.getNotesExtension()
p = md.getNotesPath()
query = Tools.getArgv(1)

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
            title='%s' % tag,
            subtitle=u"{0} Hit(s), (\u2318 to paste tag into frontmost app)".format(counter),
            valid=True,
            arg='#{0}'.format(tag)
        )
        wf.setIcon('icons/hashtag.png', 'image')
        wf.addMod(
            key='cmd',
            arg='#{0} '.format(tag),
            subtitle='Paste Tag into frontmost app',
            icon_path='icons/paste.png',
            icon_type='image'
        )
        wf.addModsToItem()
        wf.addItem()
else:
    wf.setItem(
        title="No Tags found!",
        subtitle="No Tags matches search term",
        valid=False
    )
    wf.addItem()

wf.write()
