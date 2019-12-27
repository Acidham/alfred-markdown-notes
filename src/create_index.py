#!/usr/bin/python
import os
import sys
from urllib import pathname2url

from Alfred import Items, Tools
from MyNotes import NewNote, Search
from QuerySplitter import QuerySplitter


def get_mdfiles_list_content():
    """
    Get markdown links in unordered markdown list
    
    Returns:
        str: Markdown unordered list 
    
    """
    ns = Search()
    output = list()
    files = os.getenv('files').split('|')
    for f in files:
        # query = sys.argv[1]
        link_title = ns.getNoteTitle(f)
        file_name = os.path.basename(f)
        output.append('* [' + link_title + '](' + pathname2url(file_name) + ')')
    return("\n".join(output))


query = Tools.getArgv(1)
qs = QuerySplitter(query)

MyNote = NewNote(qs.title, tags=qs.tags, content=get_mdfiles_list_content())
md_path = MyNote.create_note()
sys.stdout.write(md_path)
