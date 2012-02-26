from django.db import models

class Client(models.Model):
    '''
    Client robot model.
    '''
    name = models.CharField(max_length = 50)
    module_name = models.CharField(max_length = 50)
    last_update = models.DateTimeField()

