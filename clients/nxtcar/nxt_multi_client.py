from nxt.motor import *
import nxt, thread, httplib, simplejson, thread, time

SERVER = '192.168.0.124:5000'

def brick_register(name):
    conn = httplib.HTTPConnection(SERVER)
    req = '/dcu?name=%s&module=nxtcar' % str(name)
    res = conn.request('GET', req)
    res = conn.getresponse()
    if res.status == 200:
        return simplejson.loads(res.read())['uid']
    else:
        print res.reason
        print res.read()
        return None

def brick_proc(uid, brick):
    left_motor = Motor(brick, PORT_B)
    right_motor = Motor(brick, PORT_A)
    while 1:
        conn = httplib.HTTPConnection(SERVER)
        req = '/dcu?uid=%s&get=motors' % uid
        res = conn.request('GET', req)
        res = conn.getresponse()
        if res.status == 200:
            motors = simplejson.loads(res.read())
            left_motor.run(motors['left'])
            right_motor.run(motors['right'])
        time.sleep(1)

if __name__ == '__main__':
    for s in nxt.locator.find_bricks():
        brick = s.connect()
        name, host, signal_strength, user_flash = brick.get_device_info()
        print 'I find %s with name %s!' % (host, name)
        host = "".join(host.split(":"))
        uid = brick_register(host)
        print 'For %s received uid = %s' % (host, uid)
        if uid:
            thread.start_new_thread(brick_proc, (uid, brick))
        print '----------------'

    while 1:
        time.sleep(100)
