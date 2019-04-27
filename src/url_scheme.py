#! /usr/bin/python

import os
import sys

import MyNotes
from Alfred import Tools

f_path = Tools.getArgv(1)

url_scheme_path = MyNotes.Search.getUrlScheme(f_path)
filename = os.path.basename(f_path)
#url_scheme_path = MyNotes.Search.getUrlScheme(filename)
md_link = "[%s](%s)" % (filename,url_scheme_path)

sys.stdout.write(md_link)


