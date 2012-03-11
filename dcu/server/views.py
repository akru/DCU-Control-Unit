from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib import auth
import module_loader
import models

def main_page(request):
    '''
    Render main page.
    '''
    return render_to_response("base.html", {"user": request.user})

@csrf_exempt
def dcu_handler(request):
    '''
    DCU Handler for external devices.
    '''
    if "server" in request.POST:
        req = simplejson.loads(request.POST["server"])
        error = module_loader.test(req["module_name"], req["version"])
        if error:
            return HttpResponse(simplejson.dumps({"server":{"status": error}}),
                                                     "application/x-javascript")
        else:
            models.register(req["name"], req["module_name"])
            res = module_loader.get_module(req["module_name"]).proxy(req["name"], request.POST)
            return HttpResponse(simplejson.dumps({"server":{"status": "OK"}, "client": res}),
                                                     "application/x-javascript")
    return HttpResponse(status = 400)

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
            elif request.user.is_authenticated:
                if request.GET["server"] == "logout":
                    auth.logout(request)
                    return HttpResponse(simplejson.dumps({"logout": True}), "application/x-javascript")
                elif request.GET["server"] == "clist":
                    clist_template = get_template("clist.html")
                    clist_html = clist_template.render(Context({"clist": models.get_free_clients()}))
                    return HttpResponse(simplejson.dumps({"html": clist_html}), "application/x-javascript")
                elif request.GET["server"] == "cview":
                    module_views = module_loader.get_views(request.GET["module_name"])
                    cview_html = module_views.main()
                    return HttpResponse(simplejson.dumps({"html": cview_html}), "application/x-javascript")
                elif request.GET["server"] == "cstart" and "name" in request.GET:
                    res = models.set_user(request.GET["name"], request.user.username)
                    return HttpResponse(simplejson.dumps({"server": res}), "application/x-javascript")
                elif request.GET["server"] == "cstop" and "name" in request.GET:
                    res = models.unset_user(request.GET["name"], request.user.username)
                    return HttpResponse(simplejson.dumps({"server": res}), "application/x-javascript")
            else:
                return HttpResponse(status = 403)
        elif "client" in request.GET:
            if request.user.is_authenticated:
                if "name" in request.GET and "module_name" in request.GET:
                    mod = module_loader.get_module(request.GET["module_name"])
                    res = mod.ajax(request.GET["name"], request.GET)
                    return HttpResponse(simplejson.dumps({"client": res}), "application/x-javascript")
            else:
                return HttpResponse(status = 403)
    return HttpResponse(status = 400)

