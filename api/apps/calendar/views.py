import os
import logging
import httplib2
from django.conf import settings
from apiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from api.apps.calendar.models import CredentialsModel
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '../../settings/local/', 'client_secrets.json')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri='http://localhost:8000/oauth2callback')


@login_required
def index(request):
  storage = Storage(CredentialsModel, 'id', request.user, 'credential')
  credential = storage.get()
  if credential is None or credential.invalid == True:
    FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
    authorize_url = FLOW.step1_get_authorize_url()
    return HttpResponseRedirect(authorize_url)
  else:
    http = httplib2.Http()
    http = credential.authorize(http)
    service = build(serviceName='calendar', version='v3', http=http)
    #calendar_list_entry = service.events().get(calendarId='m34oqodtv10qvks0ntm43o0b10@group.calendar.google.com').execute()
    page_token = None
    events = service.events().list(calendarId='m34oqodtv10qvks0ntm43o0b10@group.calendar.google.com', pageToken=page_token).execute()
    return render_to_response('calendar/list_events.html',{ 'items': events['items'] })
    #service = build("plus", "v1", http=http)
    #activities = service.activities()
    #activitylist = activities.list(collection='public', userId='me').execute()
    #logging.info(activitylist)
    #return render_to_response('calendar/welcome.html', {
    #    'activitylist': activitylist,
    #    })

@login_required
def auth_return(request):
  if not xsrfutil.validate_token(settings.SECRET_KEY, request.GET['state'],
                                 request.user):
    return  HttpResponseBadRequest()
  credential = FLOW.step2_exchange(request.REQUEST)
  storage = Storage(CredentialsModel, 'id', request.user, 'credential')
  storage.put(credential)
  return HttpResponseRedirect("/")

def js(request):
    return render_to_response('calendar/js_list_events.html')
