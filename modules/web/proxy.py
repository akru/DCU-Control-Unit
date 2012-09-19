# -*- coding: utf-8 -*-
from flask import render_template, make_response, request
from dcu import Client


def draw_client_list():
    clist = Client.query.all()
    return render_template('web_client_list.html', clist=clist)

make_html = {
    'client_list': draw_client_list,
}

def run(client):
    if 'get' in request.values:
        req = request.values['get']
        try:
            return make_html[req]()

        except IndexError:
            return make_response('Unknown get request', 400)
    return render_template('web_base.html', client=client)
