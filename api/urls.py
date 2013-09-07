from django.conf.urls import patterns, include, url
from django.contrib.auth.forms import AuthenticationForm
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'api.views.home', name='home'),
    # url(r'^api/', include('api.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/$', 'api.apps.consumer.views.access', name='access'),
    url(r'^get/', 'api.apps.consumer.views.get_token', name='get_token'),
    url(r'^$', 'api.apps.calendar.views.index', name='home'),
    url(r'^js$', 'api.apps.calendar.views.js', name='js'),
    url(r'^oauth2callback', 'api.apps.calendar.views.auth_return', name='callback'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'calendar/login.html'}),

)
