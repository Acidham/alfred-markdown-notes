#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

import MyNotes
from Alfred import Tools
from QuerySplitter import QuerySplitter

query = Tools.getArgv(1)
# Read template path from previous wf step in case template ws choosen
template = Tools.getEnv('template_path')
if query.isspace():
    query = "My Note {today}".format(today=MyNotes.getTodayDate(fmt='%d_%m_%Y %H_%M_%S'))
qs = QuerySplitter(query)

if query:
    Note = MyNotes.NewNote(qs.title, template_path=template, tags=qs.tags)
    fPath = Note.create_note()
    sys.stdout.write(fPath)
