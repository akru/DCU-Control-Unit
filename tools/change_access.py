#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, simplejson
from os.path import abspath, dirname
sys.path.append('%s/..' % abspath(dirname(__file__)))
from dcu import db, Client

################################################################################
##
##  Simple client access editor.
##
################################################################################

if __name__ == '__main__':
    try:
        c = Client.query.filter_by(name=sys.argv[1]).first()
        if not c:
            print 'Client \'%s\' does not exist' % sys.argv[1]
            sys.exit(1)

        if len(sys.argv) == 2:
            print c.name, " ", simplejson.loads(c.access)
            sys.exit(0)

        access = []
        index = 2
        while len(sys.argv) > index:
            user = Client.query.filter_by(name=sys.argv[index]).first()
            if not user:
                print 'Client \'%s\' does not exist' % sys.argv[index]
                sys.exit(1)
            access.append(user.name)
            index = index + 1

        c.access = simplejson.dumps(access)
        db.session.add(c)
        db.session.commit()

    except IndexError:
        print 'USAGE: change_access.py [USER] [ACCESS_USER0] [ACCESS_USER1] ...'
