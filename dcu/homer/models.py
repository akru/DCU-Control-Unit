from django.db import models
from django.utils import simplejson

class Homer(models.Model):
    name = models.CharField(max_length=50)
    control_left = models.IntegerField()
    control_right = models.IntegerField()
    
  
def getData(request):
    return 0

def ajax(name, client):
    control = json.loads(client)
    try:
        h = Homer.objects.get(name = name)
    except:
        h = Homer(name = name, control_left = control["track_left"], control_right = control["track_right"])
        
    h.control_left = control["track_left"]
    h.control_right = control["track_right"]
    
    h.save()
    return 1
    
def proxy (name, request):
    
    try:
        h = Homer.objects.get(name = name)
    except:
        h = Homer(name = name, control_left = 0, control_right = 0)
    
    tc = { 'track_left': h.control_left, 'track_right': h.control_right }
    return tc
