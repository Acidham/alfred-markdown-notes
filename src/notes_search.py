#!/usr/bin/python

import urllib

import MyNotes
from Alfred import Items as Items
from Alfred import Tools as Tools


def get_search_config(q):
    if '&' in q:
        s_terms = q.split('&')
        s_type = 'and'
    elif '|' in q:
        s_terms = q.split('|')
        s_type = 'or'
    else:
        s_terms = [q]
        s_type = 'or'
    return s_terms, s_type


# create MD search object
md_search = MyNotes.Search()

# Load Env variables
ext = md_search.getNotesExtension()
p = md_search.getNotesPath()
query = Tools.getArgv(1)

# Get Search config with AND and OR
search_terms, search_type = get_search_config(query)

# create WF object
wf = Items()

# run search of search term(s)
if len(search_terms) > 0:
    search_results_list = list()
    sorted_file_list = md_search.searchInFiles(search_terms, search_type)
    search_results_list.extend(sorted_file_list)

    # Write search results into WF object

    for f in search_results_list:
        c_date = Tools.getDateStr(f['ctime'])
        m_date = Tools.getDateStr(f['mtime'])
        # md_path = urllib.pathname2url(f['filename'])
        md_path = f['filename'].replace(' ', '%20')
        url_scheme_path = md_search.getUrlScheme(f['path'])
        wf.setItem(
            title=f['title'],
            subtitle="Created: %s, Modified: %s" % (c_date, m_date),
            type='file',
            arg=f['path']
        )
        # Mod for CTRL - delete a Note
        wf.addMod(
            key="ctrl",
            arg=Tools.strJoin(f['path'], '|', query),
            subtitle="Delete Note",
            valid=True,
            icon_path="icons/delete.png",
            icon_type="image"
        )
        wf.addModsToItem()
        # Mod for CMD - get markdown link to Note
        wf.addMod(
            key='cmd',
            arg='[%s](%s)' % (f['filename'], md_path),
            subtitle='Copy Markdown Link to Clipboard',
            valid=True,
            icon_path='icons/link.png',
            icon_type='image'
        )
        wf.addModsToItem()
        # Mod for ALT - Export to Evernote
        wf.addMod(
            key='alt',
            arg=f['path'],
            subtitle='Export Note to Evernote',
            valid=True,
            icon_path='icons/evernote.png',
            icon_type='image'
        )
        wf.addModsToItem()
        # Mod for FN - open in Marked 2
        wf.addMod(
            key='fn',
            arg=f['path'],
            subtitle='Open Preview in Marked 2',
            valid=True,
            icon_path='icons/marked.png',
            icon_type='image'
        )
        wf.addModsToItem()
        wf.addItem()

    i = wf.getItems(response_type="dict")['items']
    if len(i) == 0:
        wf.setItem(
            title="Nothing found...",
            subtitle="Try again",
            valid=False
        )
        wf.addItem()

    wf.write()
