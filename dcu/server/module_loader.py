from django.db import models
from django.utils import importlib

def test(module_name, version):
    '''
    Return False if module version exist.
    '''
    try:
        app = models.get_app(module_name, True)
        appver = importlib.import_module(app.__name__[:-6] + "about").version()
        if appver == version:
            return False
        else:
            return "unsupport-version"
    except:
        return "unreg-module"

def get_about(module_name):
    '''
    Return information about module.
    '''
    app = models.get_app(module_name)
    return importlib.import_module(app.__name__[:-6] + "about")

def get_views(module_name):
    '''
    Return module views.
    '''
    app = models.get_app(module_name)
    return importlib.import_module(app.__name__[:-6] + "views")

def get_module(module_name):
    '''
    Return module models.
    '''
    return models.get_app(module_name)
