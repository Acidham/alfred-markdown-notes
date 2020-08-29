#!/usr/bin/python3
import os
import sys
from urllib.request import pathname2url

from Alfred3 import Tools
from MyNotes import NewNote, Search
from QuerySplitter import QuerySplitter


def get_mdfiles_list_content() -> str:
    """
    Get markdown links in unordered markdown list

    Returns:

        str: Markdown unordered list

    """
    ns = Search()
    output = list()
    files = os.getenv('files').split('|')  # one or list of md file paths from prev wf step
    for f in files:
        link_title = ns.getNoteTitle(f)
        file_name = os.path.basename(f)
        output.append(f'* [{link_title}]({pathname2url(file_name)})')
    return("\n".join(output))


query = Tools.getArgv(1)  # Title of the Note
qs = QuerySplitter(query)

MyNote = NewNote(qs.title, tags=qs.tags, content=get_mdfiles_list_content())
md_path = MyNote.createNote()
sys.stdout.write(md_path)
