from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib import auth

def main_page(request):
    '''
    Render main page of DCU.
    '''
    return render_to_response("base.html", {"user": request.user})

def dcu_handler(request):
    '''
    DCU Handler for external devices.
    '''
    return HttpResponse("Hello!!!! World!!!")

def ajax_handler(request):
    '''
    Main AJAX Handler.
    '''
    if request.is_ajax():
        if "server" in request.GET:
            if request.GET["server"] == "login" and "name" in request.GET and "password" in request.GET:
                user = auth.authenticate(username=request.GET["name"], password=request.GET["password"])
                if user is not None and user.is_active:
                    auth.login(request, user)
                    return HttpResponse(simplejson.dumps({"auth": True, "name": user.username}), 
                                                                    "application/x-javascript")
                else:
                    return HttpResponse(simplejson.dumps({"auth": False}), "application/x-javascript")
            elif request.GET["server"] == "logout":
                auth.logout(request)
                return HttpResponse(simplejson.dumps({"logout": True}), "application/x-javascript")
            
        elif "client" in request.GET:
            pass
    return HttpResponse(status = 400)
