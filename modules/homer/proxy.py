# -*- coding: utf-8 -*-
from flask import request, render_template
from simplejson import dumps
from dcu import db

class HOMER(db.Model):
    __tablename__ = 'homers'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(36), unique = True)
    m_left = db.Column(db.Integer())
    m_right = db.Column(db.Integer())

    def __init__(s, uid):
        s.uid = uid
        s.m_left = 0
        s.m_right = 0

def run(client):
    if 'get' in request.values:
        req = request.values['get']
        if req == 'motors':
            homer = HOMER.query.filter_by(uid=client.uid).first()
            if homer:
                return dumps((homer.m_left, homer.m_right))
            else:
                c = HOMER(client.uid)
                db.session.add(c)
                db.session.commit()
                return dumps((0, 0))

    elif 'motor' in request.values and 'speed' in request.values:
        h = HOMER.query.filter_by(uid=client.uid).first()
        if request.values['motor'] == 'left':
            h.m_left = request.values['speed']
        elif request.values['motor'] == 'right':
            h.m_right = request.values['speed']

        db.session.add(h)
        db.session.commit()
        return dumps(True)

    return render_template('homer_base.html', client=client)
