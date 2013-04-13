# -*- coding: utf-8 -*-
from modules.unicycle import Unicycle
from simplejson import dumps

class HOMER(Unicycle):
    __template__ = 'homer_base.html'

def run(client):
    homer = HOMER.query.filter_by(uid=client.uid).first()
    if homer is None:
        ''' If item does not exist - create it '''
        HOMER(client.uid).save()
        return dumps((0, 0))

    return homer.controlHandler(client)

