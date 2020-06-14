#!/usr/bin/python
# -*- coding: utf-8 -*-

import MyNotes
from Alfred import Items, Tools


def get_template_tag():
    tt = Tools.getEnv('template_tag')
    if '#' not in tt or tt == str():
        tt = '#Template'
    return tt


SUFFIX = " (DEFAULT)"

# create MD search object
my_notes = MyNotes.Search()

# Load env variables
ext = my_notes.getNotesExtension()
# p = my_notes.getNotesPath()
query = Tools.getArgv(1)
default_template = Tools.getEnv('default_template')
template_tag = get_template_tag()

# Get Files sorted in Notes directory
all_files = my_notes.getFilesListSorted()
template_files = sorted(all_files, key=lambda x: x['filename'] != default_template)

wf = Items()
for md_file in template_files:
    if my_notes.isNoteTagged(md_file['path'], template_tag) and query in md_file['filename']:
        suffix = str()
        if md_file['filename'] == default_template:
            suffix = SUFFIX
        wf.setItem(
            title=md_file['filename'] + suffix,
            subtitle="Create new file based on \"{0}\"".format(md_file['filename']),
            arg=Tools.strJoin(md_file['path']),
            type='file'
        )
        wf.addItem()
wf.write()
