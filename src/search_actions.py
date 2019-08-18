#!/usr/bin/python

import MyNotes
from Alfred import Items, Tools

note_path = Tools.getEnv("path_query1")
query = Tools.getEnv("path_query2")
md_notes = MyNotes.Search()
note_title = md_notes.getNoteTitle(note_path)
back_query = "<EMPTY>" if not query else query

ACTIONS = [
    {
        "title": "Back",
        "subtitle": "Back to Search with query: {0}".format(back_query),
        "arg": "{0}|{1}".format("back", query),
        "icon": "icons/back.png"
    },
    {
        "title": "Markdown Link",
        "subtitle": "Copy MD Link for \"{0}\" to the Clipboard".format(note_title),
        "arg": "{0}|[{1}]({2})".format("link", note_title, note_path),
        "icon": "icons/link.png"
    },
    {
        "title": "Evernote",
        "subtitle": "Export \"{0}\" to Evernote".format(note_title),
        "arg": "{0}|{1}".format("evernote", note_path),
        "icon": "icons/evernote.png"
    },
    {
        "title": "Marked 2",
        "subtitle": "Open Preview in Marked 2",
        "arg": "{0}|{1}".format("marked", note_path),
        "icon": "icons/marked.png"
    },
    {
        "title": "Url Scheme",
        "subtitle": "Copy Url Scheme as Markdown Link to Clipboard",
        "arg": "{0}|{1}".format("urlscheme", note_path),
        "icon": "icons/link.png"
    },
    {
        "title": "Delete Note",
        "subtitle": "Delete \"{0}\". This action cannot be undone!".format(note_title),
        "arg": "{0}|{1}>{2}".format("delete", note_path, "test"),
        "icon": "icons/delete.png"
    },
]


wf = Items()
for a in ACTIONS:
    wf.setItem(
        title=a.get("title"),
        subtitle=a.get("subtitle"),
        arg=a.get("arg")
    )
    wf.setIcon(m_path=a.get("icon"), m_type="image")
    wf.addItem()
wf.write()
