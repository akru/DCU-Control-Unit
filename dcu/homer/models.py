from django.db import models
from django.utils import simplejson

class Homer(models.Model):
    name = models.CharField(max_length=50)
    control_left = models.IntegerField()
    control_right = models.IntegerField()
    
def ajax(name, client):
    try:
        h = Homer.objects.get(name = name)
        h.control_left = client["track_left"]
        h.control_right = client["track_right"]
    except:
        h = Homer(name = name, control_left = client["track_left"], control_right = client["track_right"])
    h.save()
    return 1
    
def proxy (name, request):
    try:
        h = Homer.objects.get(name = name)
    except:
        h = Homer(name = name, control_left = 0, control_right = 0)
    tc = { 'track_left': h.control_left, 'track_right': h.control_right }
    return tc
