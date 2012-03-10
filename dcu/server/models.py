from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Client(models.Model):
    '''
    Client robot model.
    '''
    name = models.CharField(max_length = 50)
    module_name = models.CharField(max_length = 50)
    last_update = models.DateTimeField()
    user = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.name


def register(name, module_name):
    '''
    Robot registration.
    '''
    try:
        client = Client.objects.get(name=name)
    except Client.DoesNotExist:
        client = Client(name=name, module_name=module_name, last_update=datetime.now(), user="")

    if client.user != "":
        try:
            user = User.objects.get(username=client.user)
            if not user.is_authenticated():
                client.user = ""
        except Client.DoesNotExist:
            client.user = ""

    client.last_update = datetime.now()
    client.save()

def get_free_clients():
    '''
    Return list of unused robots.
    '''
    return Client.objects.filter(user="")

def set_user(name, username):
    '''
    Set user for ontrol robot.
    '''
    try:
        client = Client.objects.get(name=name)
    except Client.DoesNotExist:
        return "notexist"
    if client.user != "":
        return "inuse:"+client.user
    client.user = username
    client.save()
    return "OK"

def unset_user(name, username):
    '''
    Delete user record from robot.
    '''
    try:
        client = Client.objects.get(name=name)
    except Client.DoesNotExist:
        return "notexist"
    if username != client.user:
        return "inuse:" + client.user
    client.user = ""
    client.save()
    return "OK"

