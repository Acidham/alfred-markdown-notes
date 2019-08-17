#!/usr/bin/python

import MyNotes
from Alfred import Items, Tools

note_path = Tools.getEnv("path_query1")
query = Tools.getEnv("path_query")
md_notes = MyNotes.Search()
note_title = md_notes.getNoteTitle(note_path)

ACTIONS = [
    {
        "title": "Markdown Link",
        "subtitle": "Copy MD Link to the Clipboard",
        "arg": "{0}|[{1}]({2})".format("link", note_title, note_path),
        "icon": "icons/link.png"
    },
    {
        "title": "Delete Note",
        "subtitle": "This action cannot be undone!",
        "arg": "{0}|{1}>{2}".format("delete", note_path, "test"),
        "icon": "icons/delete.png"
    },
    {
        "title": "Evernote",
        "subtitle": "Export Note to Evernote",
        "arg": "{0}|{1}".format("evernote", note_path),
        "icon": "icons/evernote.png"
    },
    {
        "title": "Marked 2",
        "subtitle": "Open Preview in Markde 2",
        "arg": "{0}|{1}".format("marked", note_path),
        "icon": "icons/marked.png"
    }
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
