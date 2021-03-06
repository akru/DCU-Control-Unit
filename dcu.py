#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, make_response, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from simplejson import dumps, loads
from uuid import uuid4
import modules

################################################################################
##
##  The DCU - server Flask implementation.
##
################################################################################

# Configuration
DEBUG = True
SECRET_KEY = 'foo'
SQLALCHEMY_DATABASE_URI = 'sqlite:///dcu_storage.db'

# Create application
app = Flask(__name__)
app.config.from_object(__name__)

# Update template loader
modules.update_template_loader(app)

# Create database
db = SQLAlchemy(app)

# Database models
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(36), unique = True)
    name = db.Column(db.String(15), unique = True)
    module = db.Column(db.String(40))
    access = db.Column(db.String(120))

    def __init__(s, name, module):
        s.uid = str(uuid4())
        s.name = name
        s.module = module
        s.access = dumps([])

    def __repr__(s):
        return '<Client %r>' % s.name

# Routes
@app.route('/')
def base_web_client():
    '''
        Render base web client.
    '''
    try:
        uid = request.cookies['uid']
    except KeyError:
        return render_template('base_web_client.html')

    try:
        recv = request.values['recv']
    except KeyError:
        return render_template('base_web_client.html', uid=uid)

    return render_template('base_web_client.html', uid=uid, recv=recv)


@app.route('/dcu', methods = ['GET', 'POST'])
def dcu_handler():
    '''
        Main DCU handler.
    '''
    if 'uid' in request.values:
        uid = request.values['uid']

        c = Client.query.filter_by(uid=uid).first()
        if c is None:
            return make_response('UID not registered', 403)

        if 'logout' in request.values:
            db.session.delete(c)
            db.session.commit()
            return make_response(dumps({'logout':True}), 200)

        if 'recv' in request.values:
            receiver = request.values['recv']

            r = Client.query.filter_by(name=receiver).first()
            if r is None:
                return make_response('Receiver not registered', 403)

            if not r.name in loads(c.access):
                return make_response('Access denied to \'%s\'' % r.name, 403)

            module = r.module
            client = r
        else:
            module = c.module
            client = c

        if module in modules.get_list():
            proxy = modules.load(module).proxy
            return proxy.run(client)
        else:
            return make_response('Unknown module \'%s\'' % c.module, 400)
    else:
        try:
            name = request.values['name']
            module = request.values['module']

            if len(name) < 4 or len(name) > 15:
                return make_response('Name error, must be from 4 to 15', 400)

            if module in modules.get_list():
                c = Client(name, module)
                db.session.add(c)
                db.session.commit()
                return make_response(dumps({'uid':c.uid}), 200)
            else:
                return make_response('Unknown module \'%s\'' % module, 400)

        except KeyError:
            return make_response('Not sended name or module', 400)

        except OperationalError as e:
            if DEBUG:
                return make_response('Database error: %s' % e, 400)
            else:
                return make_response('Database error', 400)

        except:
            return make_response('Client create unknown exception', 500)



# Self server mode
if __name__ == '__main__':
    app.run()
