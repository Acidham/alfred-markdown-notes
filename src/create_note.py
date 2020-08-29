#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys

from Alfred3 import Tools
from MyNotes import NewNote
from QuerySplitter import QuerySplitter

query = Tools.getArgv(1)  # Note title, can contain Tags → #TAG
template = Tools.getEnv('template_path')  # Read template path from previous wf step in case template ws choosen
if query.isspace():  # if query contains a SPACE aka nothing was entered
    today = NewNote.getTodayDate(fmt='%d-%m-%Y %H-%M-%S')
    query = f"My Note {today}"
qs = QuerySplitter(query)

if query:
    Note = NewNote(qs.title, template_path=template, tags=qs.tags)
    fPath = Note.createNote()
    sys.stdout.write(fPath)
