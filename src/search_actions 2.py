#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from urllib.request import pathname2url

from Alfred3 import Items, Tools
from MyNotes import Search

# Get NotePath as path_query env variable
note_path = Tools.getEnv("path_query1")
# Get query used in search markdown notes as path_query env variable
query = Tools.getEnv("path_query2")
md_notes = Search()
# Get NoteTitle for specific note
note_title = md_notes.getNoteTitle(note_path)
file_name = pathname2url(os.path.basename(note_path))
# If query in notes search was empty subtitle uses following string
back_query = "<EMPTY>" if not query else query

# Actions in ScriptFilter menu data
ACTIONS = [
    {
        "title": "Back",
        "subtitle": f"Back to Search with query: {back_query}",
        "arg": f"back|{query}",
        "icon": "icons/back.png",
        "visible": True
    },
    {
        "title": "Markdown Link",
        "subtitle": f"Copy MD Link for \"{note_title}\" to the Clipboard",
        "arg": f"link|[{note_title}]({file_name})",
        "icon": "icons/link.png",
        "visible": True
    },
    {
        "title": "Marked 2",
        "subtitle": "Open Preview in Marked 2",
        "arg": f"marked|{note_path}",
        "icon": "icons/marked.png",
        "visible": True
    },
    {
        "title": "Url Scheme",
        "subtitle": "Copy Url Scheme as Markdown Link to Clipboard",
        "arg": f"urlscheme|{note_path}",
        "icon": "icons/scheme.png",
        "visible": Tools.getEnv("url_scheme")
    },
    {
        "title": "Delete Note",
        "subtitle": f'Delete "{note_title}". This action cannot be undone!',
        "arg": f"delete|{note_path}>{query}",
        "icon": "icons/delete.png",
        "visible": True
    },
]

# Generate ScriptFilter Output
wf = Items()
for a in ACTIONS:
    val = a.get('visible')
    if val:
        wf.setItem(
            title=a.get("title"),
            subtitle=a.get("subtitle"),
            arg=a.get("arg")
        )
        wf.setIcon(m_path=a.get("icon"), m_type="image")
        wf.addItem()
wf.write()
