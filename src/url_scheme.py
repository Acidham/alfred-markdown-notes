#! /usr/bin/python

import os
import sys

from Alfred import Tools
from MyNotes import Search

f_path = Tools.getArgv(1)

url_scheme_path = Search.getUrlScheme(f_path)
filename = os.path.basename(f_path)
# url_scheme_path = MyNotes.Search.getUrlScheme(filename)
md_link = "[{0}]({1})".format(filename, url_scheme_path)

sys.stdout.write(md_link)
