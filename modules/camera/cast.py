# -*- coding: utf-8 -*-
import subprocess, pickle, os

def run(source_port, public_uid):
    dest_dir = '/tmp/camera/' + public_uid
    os.mkdir(dest_dir)
    return pickle.dumps(subprocess.Popen(['vcaps', '%d' % source_port, '%s' % dest_dir ]))

def stop(pid):
    p = pickle.loads(pid)
    p.kill()
    p.wait()
