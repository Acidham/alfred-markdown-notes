#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from unicodedata import normalize

from Alfred3 import Items as Items
from Alfred3 import Keys as K
from Alfred3 import Tools as Tools
from MyNotes import Search

CMD = u'\u2318'
SHIFT = u'\u21E7'

# create MD search object
md_search = Search()

query = normalize('NFC', Tools.getArgv(1))

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
        subtitle=f"Created: {c_date}, Modified: {m_date} ({K.CMD} Actions, {K.SHIFT} Quicklook)",
        type='file',
        arg=f['path']
    )
    # Mod for CMD - new action menu
    wf.addMod(
        key="cmd",
        arg=f"{f['path']}>{query}",
        subtitle="Enter Actions Menu for the Note...",
        icon_path="icons/action.png",
        icon_type="image"
    )
    wf.addItem()

if len(wf.getItems(response_type="dict")['items']) == 0:
    wf.setItem(
        title="Nothing found...",
        subtitle=f'Do you want to create a new note with title "{query}"?',
        arg=query
    )
    wf.addItem()
wf.write()
