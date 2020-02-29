#!/usr/bin/python
# -*- coding: utf-8 -*-

from Alfred import Items, Tools
from MyNotes import Search

# Get NotePath as path_query env variable
note_path = Tools.getEnv("path_query1")
# Get query used in search markdown notes as path_query env variable
query = Tools.getEnv("path_query2")
md_notes = Search()
# Get NoteTitle for specific note
note_title = md_notes.getNoteTitle(note_path)
# If query in notes search was empty subtitle uses following string
back_query = "<EMPTY>" if not query else query

# Actions in ScriptFilter menu data
ACTIONS = [
    {
        "title": "Back",
        "subtitle": "Back to Search with query: {0}".format(back_query),
        "arg": "{0}|{1}".format("back", query),
        "icon": "icons/back.png",
        "visible": True
    },
    {
        "title": "Markdown Link",
        "subtitle": u"Copy MD Link for \"{0}\" to the Clipboard".format(note_title),
        "arg": u"{0}|[{1}]({2})".format("link", note_title, note_path),
        "icon": "icons/link.png",
        "visible": True
    },
    {
        "title": "Evernote",
        "subtitle": u"Export \"{0}\" to Evernote".format(note_title),
        "arg": "{0}|{1}".format("evernote", note_path),
        "icon": "icons/evernote.png",
        "visible": Tools.getEnv("evernote_auth_token")
    },
    {
        "title": "Marked 2",
        "subtitle": "Open Preview in Marked 2",
        "arg": "{0}|{1}".format("marked", note_path),
        "icon": "icons/marked.png",
        "visible": True
    },
    {
        "title": "Url Scheme",
        "subtitle": "Copy Url Scheme as Markdown Link to Clipboard",
        "arg": "{0}|{1}".format("urlscheme", note_path),
        "icon": "icons/scheme.png",
        "visible": Tools.getEnv("url_scheme")
    },
    {
        "title": "Delete Note",
        "subtitle": u"Delete \"{0}\". This action cannot be undone!".format(note_title),
        "arg": "{0}|{1}>{2}".format("delete", note_path, query),
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
