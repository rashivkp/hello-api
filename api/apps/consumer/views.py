from django.http import HttpResponseRedirect, HttpResponse
from models import Agent
from django.conf import settings
from rauth.service import OAuth1Service

CONSUMER_KEY = settings.CONSUMER['consumer_key']
CONSUMER_SECRET = settings.CONSUMER['consumer_secret']
REQUEST_TOKEN_URL = 'https://bitbucket.org/!api/1.0/oauth/request_token'
ACCESS_TOKEN_URL = 'https://bitbucket.org/!api/1.0/oauth/access_token'
AUTHORIZE_URL = 'https://bitbucket.org/!api/1.0/oauth/authenticate'
CALL_BACK = 'http://127.0.0.1:8000/get/'


def get_session():

    # Create the service
    bitbucket = OAuth1Service(name='bitbucket',
                              consumer_key=CONSUMER_KEY,
                              consumer_secret=CONSUMER_SECRET,
                              request_token_url=REQUEST_TOKEN_URL,
                              access_token_url=ACCESS_TOKEN_URL,
                              authorize_url=AUTHORIZE_URL)

    # Make the request for a token, include the callback URL.
    rtoken, rtoken_secret = bitbucket.get_request_token(params={'oauth_callback': CALL_BACK})

    agent = Agent.objects.get(pk=1)
    agent.consumer_key = CONSUMER_KEY
    agent.consumer_secret = CONSUMER_SECRET
    agent.token = rtoken
    agent.token_secret = rtoken_secret
    agent.save()

    # Use the token to rquest an authorization URL.
    authorize_url = bitbucket.get_authorize_url(rtoken)

    # Send the user to Bitbucket to authenticate. The CALL_BACK is the
    # URL. The URL is redirected to after success. Normally, your
    # application automates this whole exchange.
    return authorize_url, bitbucket


def access():
    print "%s" % settings.CONSUMER['name']

def get_token(request):
    if request.GET.get('oauth_verifier', '') != '':
        bitbucket = OAuth1Service(name='bitbucket',
                              consumer_key=CONSUMER_KEY,
                              consumer_secret=CONSUMER_SECRET,
                              request_token_url=REQUEST_TOKEN_URL,
                              access_token_url=ACCESS_TOKEN_URL,
                              authorize_url=AUTHORIZE_URL)
        agent = Agent.objects.get(pk=1)
        oauth_verifier = request.GET.get('oauth_verifier', '')
        session = bitbucket.get_auth_session(agent.token, agent.token_secret, data={'oauth_verifier': oauth_verifier})
        username = 'rashivkp'
        repo_slug = 'peecs'

        url = 'https://api.bitbucket.org/1.0/repositories/%s/%s/branches' % (username, repo_slug)
        resp = session.get(url)
        return HttpResponse(resp.json())
    else:
        authorize_url, request.session['bitbucket'] = get_session()

    return HttpResponseRedirect(authorize_url)

