#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import abspath, dirname
import sys

################################################################################
##
##  Simple module tester
##
################################################################################

if __name__ == '__main__':
    sys.path.append('%s/..' % abspath(dirname(__file__)))
    from modules import get_list, load

    print '=> DCU-F Module tester <='

    for module in get_list():
        print '==> %s: Test started...' % module
        load(module).test.start()
