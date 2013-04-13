# -*- coding: utf-8 -*-
from flask import make_response, render_template, request
from simplejson import dumps
from math import sin, cos
from dcu import db

################################################################################
##
##  Simple unicycle model.
##
################################################################################

class Unicycle(db.Model):
    '''
        The base unicycle datastorage model
    '''
    id = db.Column(db.Integer, primary_key=True)
    ''' Unical identificator of client '''
    uid = db.Column(db.String(36), unique=True)
    ''' Linear speed '''
    radius = db.Column(db.Integer)
    ''' Orientation angle '''
    angle = db.Column(db.Integer)
    ''' Control handler '''
    __handler__ = {
        'get': {
            'raw': lambda s: (s.radius, s.angle),
            'differential': lambda s: (s.radius + s.angle, s.radius - s.angle),
        },
        'set': {
            'radius': lambda s, args: s.save(radius=int(args[0])),
            'angle': lambda s, args: s.save(angle=int(args[0])),
            'all': lambda s, args: s.save(radius=int(args[0]), angle=int(args[1]))
        }
    }

    def __init__(s, uid, radius=0, angle=0):
        ''' 
            Model initialisation 
        '''
        s.uid = uid
        s.radius = radius
        s.angle = angle

    def save(s, radius=None, angle=None):
        '''
            Save model data to storage
        '''
        if radius:
            s.radius = radius
        if angle:
            s.angle = angle

        db.session.add(s)
        return db.session.commit()

    def controlHandler(s, client):
        '''
            Handler for control requests
        '''
        req = request.values
        try:
            if 'get' in req:
                return dumps(s.__handler__['get'][req['get']](s))

            elif 'set' in req:
                return dumps(s.__handler__['set'][req['set']](s, req.getlist('args[]')))

            else:
                return render_template(s.__template__, client=client)
        
        except KeyError:
            return make_response('Bad request', 400)

