#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alfred3 import Items as Items
from Alfred3 import Tools as Tools
from MyNotes import Search

# create MD search object
md_search = Search()

query = Tools.getArgv(1)  # Search Term(s)

# Get Search config with AND and OR
search_terms, search_type = md_search.get_search_config(query)

# create WF object
wf = Items()

# exec search if search terms were entered
if len(search_terms) > 0:
    sorted_file_list = md_search.notes_search(search_terms, search_type)
# get full list of file in case no search was entered
else:
    sorted_file_list = md_search.getFilesListSorted()
# Write search results into WF object
for f in sorted_file_list:
    c_date = Tools.getDateStr(f['ctime'])
    m_date = Tools.getDateStr(f['mtime'])
    wf.setItem(
        title=f['title'],
        subtitle=u"Created: {0}, Modified: {1} ({2} Actions, {3} Quicklook)".format(
            c_date, m_date, u'\u2318', u'\u21E7'),
        type='file',
        arg=f['path']
    )
    # Mod for CMD - new action menu
    wf.addMod(
        key="cmd",
        arg="{0}>{1}".format(f['path'], query),
        subtitle="Enter Actions Menu for the Note...",
        icon_path="icons/action.png",
        icon_type="image"
    )
    wf.addItem()

if len(wf.getItems(response_type="dict")['items']) == 0:
    wf.setItem(
        title="Nothing found...",
        subtitle="Do you want to create a new note with title \"{0}\"?".format(query),
        arg=query
    )
    wf.addItem()
wf.write()
