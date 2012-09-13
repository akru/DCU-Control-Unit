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
        assert 'Not sended name or module' in res.data

        res = s.app.get('/dcu?name=test')
        assert 'Not sended name or module' in res.data

        res = s.app.get('/dcu?module=utest')
        assert 'Not sended name or module' in res.data

        res = s.app.get('/dcu?name=test&module=te')
        assert 'Unknown module \'te\'' in res.data

        res = s.app.get('/dcu?name=test&module=utest')
        uid = loads(res.data)['uid']
        assert uid
        print 'registered uid: %s' % uid

        res = s.app.get('/dcu?name=test&module=utest')
        assert 'Database exeption(m.b. name in use)' in res.data
        print 'double registration is not permitted'

        res = s.app.get('/dcu?uid=12345')
        assert 'UID not registered' in res.data

        res = s.app.get('/dcu?uid=%s&recv=foo' % uid)
        assert 'Access denied to \'foo\'' in res.data

        res = s.app.get('/dcu?uid=%s' % uid)
        assert 'receive client test' in res.data
        print 'login complete'

if __name__ == '__main__':
    unittest.main()
