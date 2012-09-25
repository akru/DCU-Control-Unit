# -*- coding: utf-8 -*-
from flask import request, render_template
from simplejson import dumps
from dcu import db

class NXTCar(db.Model):
    __tablename__ = 'nxtcars'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(36), unique = True)
    left_motor = db.Column(db.Integer())
    right_motor = db.Column(db.Integer())

    def __init__(s, uid):
        s.uid = uid
        s.left_motor = 0
        s.right_motor = 0

def run(client):
    if 'get' in request.values:
        req = request.values['get']
        if req == 'motors':
            car = NXTCar.query.filter_by(uid=client.uid).first()
            if car:
                return dumps({'left':car.left_motor, 'right':car.right_motor})
            else:
                c = NXTCar(client.uid)
                db.session.add(c)
                db.session.commit()
                return dumps({'left':0, 'right':0})

    elif 'motor' in request.values and 'speed' in request.values:
        car = NXTCar.query.filter_by(uid=client.uid).first()
        if request.values['motor'] == 'right':
            car.right_motor = request.values['speed']
        else:
            car.left_motor = request.values['speed']
        db.session.add(car)
        db.session.commit()
        return dumps(True)

    return render_template('nxtcar_base.html', client=client)
