#!/usr/bin/python

import urllib

import MyNotes
from Alfred import Items as Items
from Alfred import Tools as Tools

# create MD search object
md_search = MyNotes.Search()

# Load Env variables
ext = md_search.getNotesExtension()
p = md_search.getNotesPath()
query = Tools.getArgv(1)

# Get Search config with AND and OR
search_terms, search_type = md_search.get_search_config(query)

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
            subtitle=u"Created: {0}, Modified: {1} ({2} for Actions...)".format(
                c_date, m_date, u"\u2318"),
            type='file',
            arg=f['path']
        )
        # Mod for CMD - new action menu
        wf.addMod(
            key="cmd",
            arg="{0}>{1}".format(f['path'], query),
            subtitle="Actions Menu...",
            icon_path="icons/action.png",
            icon_type="image"
        )
        wf.addModsToItem()
        wf.addItem()

    if len(wf.getItems(response_type="dict")['items']) == 0:
        wf.setItem(
            title="Nothing found...",
            subtitle="Do you want to create a new note with title \"{0}\"?".format(query),
            arg=query
        )
        wf.addItem()
    wf.write()
