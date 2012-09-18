from flask import render_template, request
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
        return make_html[req]()
    return render_template('web_base.html', client=client)
