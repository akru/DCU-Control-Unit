#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import abspath, dirname
import sys, tempfile, os
sys.path.append('%s/..' % abspath(dirname(__file__)))

from simplejson import loads
import unittest
import dcu

################################################################################
##
##  DCU Server tests.
##
################################################################################

class DCUTestCase(unittest.TestCase):
    def setUp(s):
        s.db_fd, dbname = tempfile.mkstemp()
        dcu.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % dbname
        dcu.db.create_all()
        s.app = dcu.app.test_client()

    def tearDown(s):
        os.close(s.db_fd)

    def test_register_client(s):
        res = s.app.get('/dcu')
        assert '' in res.data

        res = s.app.get('/dcu?name=test')
        assert 'Error: not sended name or module' in res.data

        res = s.app.get('/dcu?module=utest')
        assert 'Error: not sended name or module' in res.data

        res = s.app.get('/dcu?name=test&module=te')
        assert 'Error: unknown module \'te\'' in res.data

        res = s.app.get('/dcu?name=test&module=utest')
        uid = loads(res.data)['uid']
        assert uid
        print 'registered uid: %s' % uid

        res = s.app.get('/dcu?name=test&module=utest')
        assert 'Client create unknown exception' in res.data
        print 'double registration is not permitted'

        res = s.app.get('/dcu?uid=12345')
        assert 'Error: UID does not registered' in res.data

        res = s.app.get('/dcu?uid=%s&recv=foo' % uid)
        assert 'Error: receiver does not exist' in res.data

        res = s.app.get('/dcu?uid=%s' % uid)
        assert 'receive client test' in res.data
        print 'login complete'

        res = s.app.get('/logout?uid=%s' % uid)
        assert '{\"logout\": true}' in res.data
        res = s.app.get('/dcu?uid=%s' % uid)
        assert 'Error: UID does not registered' in res.data
        print 'logout complete'

if __name__ == '__main__':
    unittest.main()
