#!/usr/bin/python

import MyNotes
from Alfred import Items as Items
from Alfred import Tools as Tools

# create MD search object
md = MyNotes.Search()

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
            subtitle="{0} Hit(s)".format(counter),
            valid=True,
            arg='#%s' % tag
        )
        wf.setIcon('icons/hashtag.png', 'image')
        wf.addItem()
else:
    wf.setItem(
        title="No Tags found!",
        subtitle="No Tags matches search term",
        valid=False
    )
    wf.addItem()

wf.write()
