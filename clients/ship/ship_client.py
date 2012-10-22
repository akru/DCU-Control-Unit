#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib, simplejson, time, bluetooth
from ship import SHIP

SERVER = '127.0.0.1:5000'
BLUETOOTH_DEVICE = '00:12:6F:22:35:44'

def ship_register():
    conn = httplib.HTTPConnection(SERVER)
    req = '/dcu?name=SHIP&module=ship'
    res = conn.request('GET', req)
    res = conn.getresponse()
    if res.status == 200:
        return simplejson.loads(res.read())['uid']
    else:
        print res.reason
        print res.read()
        return None

def ship_proc(uid, sock):
    s = SHIP(sock, '')
    while 1:
        conn = httplib.HTTPConnection(SERVER)
        req = '/dcu?uid=%s&get=motors' % uid
        res = conn.request('GET', req)
        res = conn.getresponse()
        if res.status == 200:
            control = simplejson.loads(res.read())
            s.raw_control({'drive':control})
        time.sleep(1)

def bluesock():
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((BLUETOOTH_DEVICE, 1))
    return sock

if __name__ == '__main__':
    sock = bluesock()
    uid = ship_register()
    if uid:
        ship_proc(uid, sock)
