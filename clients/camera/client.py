#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib, simplejson, subprocess, time

SERVERIP = '194.85.161.167'
MODULE = 'camera'
NAME = 'CAMERA_AKRU'

def register():
    conn = httplib.HTTPSConnection(SERVERIP)
    req = '/dcu?name=%s&module=%s' % (NAME, MODULE)
    res = conn.request('GET', req)
    res = conn.getresponse()
    if res.status == 200:
        uid = simplejson.loads(res.read())['uid']
        conn.close()
        return uid
    else:
        print res.reason
        print res.read()
        conn.close()
        return None

def proc(uid):
    conn = httplib.HTTPSConnection(SERVERIP)
    req = '/dcu?uid=%s&get=port' % uid
    res = conn.request('GET', req)
    res = conn.getresponse()
    if res.status == 200:
        port = simplejson.loads(res.read())
        conn.close()
        print 'Port:', port['source_port']

        port = port['source_port']
        subprocess.Popen(['start_vcap.sh', SERVERIP, '%s' % port], close_fds=True)
        print 'Translation started'
        while 1:
            time.sleep(1)
    else:
        print res.reason
        print res.read()
        conn.close()

if __name__ == '__main__':
    uid = register()
    print 'UID:', uid
    if uid:
        proc(uid)
