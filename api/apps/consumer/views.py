from django.http import HttpResponseRedirect, HttpResponse
from urllib2 import urlopen
from urllib import urlencode
from models import Agent

def access(request):
    return HttpResponse("Hello World!")

