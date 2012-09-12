#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, make_response, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
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

# Create small app
app = Flask(__name__)
app.config.from_object(__name__)

# Create database
db = SQLAlchemy(app)

# Database models
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(36), unique = True)
    name = db.Column(db.String(40), unique = True)
    module = db.Column(db.String(40))

    def __init__(s, name, module):
        s.uid = str(uuid4())
        s.name = name
        s.module = module

# Routes
@app.route('/')
def base_web_client():
    '''
        Render base web client.
    '''
    return render_template('base_web_client.html')

@app.route('/dcu', methods = ['GET', 'POST'])
def dcu_handler():
    '''
        Main DCU handler.
    '''
    if 'uid' in request.values:
        return make_response('You uid is %s' % request.values['uid'], 200)

    else:
        try:
            name = request.values['name']
            module = request.values['module']
            if module in modules.get_list():
                c = Client(name, module)
                db.session.add(c)
                db.session.commit()
                return make_response('uid:%s' % c.uid, 200)
            else:
                return make_response('Unknown module \'%s\'' % module, 500)

        except SQLAlchemyError:
            return make_response('Database exeption(m.b. name in use)', 500)

        except:
            return make_response('Client create unknown exception', 500)

    return make_response('Bad request', 400)

# Self server mode
if __name__ == '__main__':
    app.run()
