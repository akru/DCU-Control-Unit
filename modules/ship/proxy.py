# -*- coding: utf-8 -*-
from flask import request, render_template
from simplejson import dumps
from dcu import db

class SHIP(db.Model):
    __tablename__ = 'ships'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(36), unique = True)
    m_front = db.Column(db.Integer())
    m_middle = db.Column(db.Integer())
    m_back = db.Column(db.Integer())
    m_servo = db.Column(db.Integer())

    def __init__(s, uid):
        s.uid = uid
        s.m_front = 127
        s.m_middle = 127
        s.m_back = 127
        s.m_servo = 127

def run(client):
    if 'get' in request.values:
        req = request.values['get']
        if req == 'motors':
            ship = SHIP.query.filter_by(uid=client.uid).first()
            if ship:
                return dumps((ship.m_servo, ship.m_front, ship.m_back, ship.m_middle))
            else:
                c = SHIP(client.uid)
                db.session.add(c)
                db.session.commit()
                return dumps((127, 127, 127, 127))

    elif 'motor' in request.values and 'speed' in request.values:
        ship = SHIP.query.filter_by(uid=client.uid).first()
        if request.values['motor'] == 'front':
            ship.m_front = request.values['speed']
        elif request.values['motor'] == 'middle':
            ship.m_middle = request.values['speed']
        elif request.values['motor'] == 'back':
            ship.m_back = request.values['speed']
        else:
            ship.m_servo = request.values['speed']

        db.session.add(ship)
        db.session.commit()
        return dumps(True)

    return render_template('ship_base.html', client=client)
