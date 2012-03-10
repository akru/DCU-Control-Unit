# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Template, Context
import datetime
from django.template.loader import get_template


def main(request): 
   html = get_template('joystick.html')
   context = Context({})
   return html.render(context)
    
def joystick(request):
    html = get_template('joystick.html')
    c = Context({})
    return HttpResponse(html.render(c))
