#!/usr/bin/python

import os
import sys
from urllib import pathname2url

from MyNotes import Search

query = sys.argv[1]
file_name = os.path.basename(query)
ms = Search()
title = ms.getNoteTitle(query)
output = '[' + title + '](' + pathname2url(file_name) + ')'
sys.stdout.write(output)
