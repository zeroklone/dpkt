# $Id: dpkt.py 43 2007-08-02 22:42:59Z jon.oberheide $
# -*- coding: utf-8 -*-
"""Simple packet creation and parsing."""

import sys

# Decide which version to import based on Python version.
if sys.version_info < (3, 0):
    from dpkt2 import *
else:
    from dpkt3 import *