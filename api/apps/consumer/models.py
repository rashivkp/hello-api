from django.db import models

class Agent(models.Model):

    name = models.CharField(max_length=64)
    consumer_key = models.CharField(max_length=64)
    consumer_secret = models.CharField(max_length=64)
    token = models.CharField(max_length=64, blank=True)
    token_secret = models.CharField(max_length=64, blank=True)
    access_token = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return "%s" % (self.name)
