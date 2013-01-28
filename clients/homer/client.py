#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib, simplejson, time, socket
from homer import HOMER

SERVER = '192.168.0.11:5000'

def register():
    conn = httplib.HTTPConnection(SERVER)
    req = '/dcu?name=HOMER_001&module=homer'
    res = conn.request('GET', req)
    res = conn.getresponse()
    if res.status == 200:
        return simplejson.loads(res.read())['uid']
    else:
        print res.reason
        print res.read()
        return None

def proc(uid, sock):
    h = HOMER(sock)
    while 1:
        conn = httplib.HTTPConnection(SERVER)
        req = '/dcu?uid=%s&get=motors' % uid
        res = conn.request('GET', req)
        res = conn.getresponse()
        if res.status == 200:
            c = simplejson.loads(res.read())
            h.setTrackControl(c[0], c[1])
        time.sleep(1)

if __name__ == '__main__':
    sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('', 7777))
    uid = register()
    if uid:
        proc(uid, sock)
    else:
        print 'NOT received UID'
