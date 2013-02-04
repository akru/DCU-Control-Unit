# -*- coding: utf-8 -*-
import subprocess, pickle

def run(source_port, public_uid):
    return pickle.dumps(subprocess.Popen(['vcaps', '%d' % source_port, '%s' % public_uid ], close_fds=True))

def stop(pid):
    p = pickle.loads(pid)
    p.kill()
    p.wait()
