#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os.path import abspath, dirname
sys.path.append('%s/..' % abspath(dirname(__file__)))
import modules

################################################################################
##
## Datastorage creator.
##
################################################################################

for i in modules.get_list():
    modules.load(i)

from dcu import db
db.create_all()

