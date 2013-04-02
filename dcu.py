#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, make_response, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from simplejson import dumps, loads
from functools import wraps
from uuid import uuid4
import modules, requests

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
    '''
        The main client datastorage model
    '''
    __tablename__ = 'clients'
    ''' Primary key '''
    id = db.Column(db.Integer, primary_key=True)
    ''' UUID4 Unical ID '''
    uid = db.Column(db.String(36), unique = True)
    ''' Client Name '''
    name = db.Column(db.String(15), unique = True)
    ''' Client Module '''
    module = db.Column(db.String(40))
    ''' JSON-formatted access list '''
    access = db.Column(db.String(120))

    def __init__(s, name=None, module=None):
        '''
            Initialisation
        '''
        s.uid = str(uuid4())
        s.name = name
        s.module = module
        s.access = dumps([])

    def signup(s):
        '''
            New client registration
        '''
        try:
            name = request.values['name']
            module = request.values['module']

            if len(name) > 15:
                return make_response('Error: name is too long!', 400)

            ''' Searching module in module list '''
            if module in modules.get_list():
                ''' Create client and save into datastorage '''
                s.name, s.module = name, module
                db.session.add(s)
                db.session.commit()
                return make_response(dumps({'uid':s.uid}), 200)

            else:
                return make_response('Error: unknown module \'%s\'' % module, 400)

        except KeyError:
            ''' Name or module does not exist in request '''
            return make_response('Error: not sended name or module', 400)

        except OperationalError as e:
            ''' SQLAlchemy error '''
            if DEBUG:
                 return make_response('Database error: %s' % e, 400)
            else:
                 return make_response('Database error', 400)

        except:
            ''' Anything else =) '''
            return make_response('Client create unknown exception', 500)


# Decorators
def json_proxy(fn):
    '''
        Proxy for JSON-in-body requests
    '''
    @wraps(fn)
    def proxy(*args, **kwargs):
        if request.json is not None:
            url = url_for('dcu_handler', _external=True)
            return make_response(requests.get(url, params=request.json).text, 200)
        else:
            return fn(*args, **kwargs)
    return proxy


def uid_checker(fn):
    '''
        UID checker decorator
    '''
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'uid' in request.cookies:
            uid = request.cookies['uid']

        elif 'uid' in request.values:
            uid = request.values['uid']

        else:
            return fn(client='noset', *args, **kwargs)

        c = Client.query.filter_by(uid=uid).first()
        return fn(client=c, *args, **kwargs)
    return wrapper


def recv_checker(fn):
    '''
        Receiver checker decorator
    '''
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            recv = request.values['recv']
            r = Client.query.filter_by(name=recv).first()
            return fn(receiver=r, *args, **kwargs)

        except KeyError:
            return fn(receiver='noset', *args, **kwargs)
    return wrapper


# Routes
@app.route('/')
@uid_checker
@recv_checker
def base_web_client(client=None, receiver=None):
    '''
        Render base web client.
    '''
    return render_template('base_web_client.html', client=client, recv=receiver)


@app.route('/logout', methods = ['GET', 'POST'])
@uid_checker
def logout(client=None):
    '''
        Remove client from datastorage
    '''
    if client is not None and client != 'noset':
        db.session.delete(client)
        db.session.commit()
        return make_response(dumps({'logout':True}), 200)

    else:
        return make_response(dumps({'logout':False}), 200)


@app.route('/dcu', methods = ['GET', 'POST'])
@json_proxy
@uid_checker
@recv_checker
def dcu_handler(client=None, receiver=None):
    '''
        Main DCU handler.
    '''
    if client is 'noset':
        ''' If client no sending, trying to signup '''
        return Client().signup()

    elif client is None:
        ''' If client is sended but not found '''
        return make_response('Error: UID does not registered', 403)

    if receiver is 'noset':
        ''' If receiver is no sended - this is self-access request '''
        module = client.module

    elif receiver is None:
        ''' If receiver is sended but not found '''
        return make_response('Error: receiver does not exist', 403)

    else:
        ''' Searching receiver in access list '''
        if not receiver.name in loads(client.access):
            return make_response('Error: access denied to \'%s\'' % r.name, 403)

        ''' Change client module to receiver '''
        module = receiver.module
        client = receiver

    if module in modules.get_list():
        ''' Searching module in moule list '''
        proxy = modules.load(module).proxy
        return proxy.run(client)

    else:
        return make_response('Error: unknown module \'%s\'' % c.module, 400)


# Self-server mode
if __name__ == '__main__':
    app.run(threaded=True)
