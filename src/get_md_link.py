#!/usr/bin/python3

import os
import sys
from urllib.request import pathname2url

from MyNotes import Search

query = sys.argv[1]  # File path to MD Note
file_name = os.path.basename(query)
ms = Search()
title = ms.getNoteTitle(query)
output = f"[{title}]({pathname2url(file_name)})"
sys.stdout.write(output)
