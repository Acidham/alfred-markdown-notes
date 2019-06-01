#! /usr/bin/python

import os
import sys
from urllib import pathname2url

query = sys.argv[1]
file_name = os.path.basename(query)
output = '[' + file_name + '](' + pathname2url(file_name) + ')'
sys.stdout.write(output)
