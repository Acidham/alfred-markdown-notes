#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

from Alfred import Tools
from MyNotes import NewNote
from QuerySplitter import QuerySplitter

reload(sys)
sys.setdefaultencoding('utf-8')
query = Tools.getArgv(1).encode('utf-8')
# Read template path from previous wf step in case template ws choosen
template = Tools.getEnv('template_path')
if query.isspace():
    query = "My Note {today}".format(today=NewNote.getTodayDate(fmt='%d-%m-%Y %H-%M-%S'))
qs = QuerySplitter(query)

if query:
    Note = NewNote(qs.title, template_path=template, tags=qs.tags)
    fPath = Note.create_note()
    sys.stdout.write(fPath)
