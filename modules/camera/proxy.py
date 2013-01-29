# -*- coding: utf-8 -*-
from flask import request, render_template
from simplejson import dumps
from uuid import uuid4
from dcu import db
import cast

class Camera(db.Model):
    __tablename__ = 'cameras'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(36), unique = True)
    public_uid = db.Column(db.String(36), unique = True)
    source_port = db.Column(db.Integer())
    pid = db.Column(db.String(300))

    def __init__(s, uid):
        s.uid = uid
        s.public_uid = str(uuid4())

def run(client):
    cam = Camera.query.filter_by(uid=client.uid).first()
    if not cam:
        db.session.add(Camera(client.uid))
        db.session.commit()

        cam = Camera.query.filter_by(uid=client.uid).first()
        cam.source_port = 50000 + cam.id
        cam.pid = cast.run(cam.source_port, cam.public_uid)
        db.session.add(cam)
        db.session.commit()

    if 'get' in request.values:
        req = request.values['get']

        if req == 'port':
            return dumps({'source_port': cam.source_port})

    return render_template("camera_base.html", public_uid=cam.public_uid)
