#!/usr/bin/python3

import os
import sys

from Alfred3 import Tools
from MyNotes import Search

f_path = Tools.getArgv(1)  # Path to MD Note
s = Search()
url_scheme_path = s.getUrlScheme(f_path)
filename = os.path.basename(f_path)
md_link = f"[{filename}]({url_scheme_path})"
sys.stdout.write(md_link)
