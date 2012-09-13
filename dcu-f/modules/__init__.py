# -*- coding: utf-8 -*-
from os.path import abspath, dirname
from os import listdir, stat
from stat import S_ISDIR
import jinja2
import sys

################################################################################
##
##  Simple module lister and loader.
##
################################################################################

MODULES_DIR = abspath(dirname(__file__))

def get_list():
    for module in listdir(MODULES_DIR):
        if S_ISDIR(stat('%s/%s' % (MODULES_DIR, module)).st_mode):
            yield module

def update_template_loader(app):
    loaders = [ app.jinja_loader ]
    for module in get_list():
        l = jinja2.FileSystemLoader('%s/%s/templates' % (MODULES_DIR, module))
        loaders.append(l)
    app.jinja_loader = jinja2.ChoiceLoader(loaders)

def load(module):
    if module in get_list():
        sys.path.append(MODULES_DIR)
        return __import__(module)
    else:
        return None
