#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join
from shutil import copytree
from os import makedirs
import sys
sys.path.append('%s/..' % abspath(dirname(__file__)))
import modules

################################################################################
##
##  Static collector.
##
################################################################################

try:
    target = sys.argv[1]
    print 'Moving static files to %s ...' % target

    core_static = abspath('%s/../static' % dirname(__file__))
    print core_static
    print 'Copying core static files...'
    try:
        copytree(core_static, target)
        print 'done'
    except OSError:
        print 'pass'

    for module in modules.get_list():
        print 'Copying %s static files...' % module
        module_static = join(join(modules.MODULES_DIR, module), 'static')
        try:
            copytree(module_static, join(target, module))
            print 'done'
        except OSError:
            print 'pass'

    print 'complete! Have fun! =)'


except IndexError:
    print 'Usage:\n\tcollect_static.py [target]'
