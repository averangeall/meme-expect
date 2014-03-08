from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/explain/')),
    url(r'^init/$', 'turker.views.init'),

    url(r'^fill/$', 'turker.views.fill'),
    url(r'^show/$', 'turker.views.show'),

    url(r'^ocr/$', 'ocr.views.write'),
    url(r'^insert/$', 'ocr.views.insert'),

    url(r'^browse/$', 'browse.views.every'),
    url(r'^browse/(?P<template_name>.+)$', 'browse.views.single'),

    url(r'^reasonable/$', 'reasonable.views.show'),
    url(r'^reasonable/insert/$', 'reasonable.views.insert'),
    url(r'^reasonable/dump/$', 'reasonable.views.dump'),
    url(r'^reasonable/choose/(?P<gag_id>.+)$', 'reasonable.views.choose'),
    url(r'^reasonable/remove/(?P<gag_id>.+)$', 'reasonable.views.remove'),

    url(r'^opposite/$', 'opposite.views.show'),
    url(r'^opposite/choose/reasonable/$', 'opposite.views.choose_reasonable'),
    url(r'^opposite/choose/opposite/$', 'opposite.views.choose_opposite'),
    url(r'^opposite/upload/reasonable/$', 'opposite.views.upload_reasonable'),
    url(r'^opposite/upload/opposite/$', 'opposite.views.upload_opposite'),
    url(r'^opposite/insert/$', 'opposite.views.insert'),
    url(r'^opposite/dump/$', 'opposite.views.dump'),

    url(r'^explain/$', 'explain.views.show'),
    url(r'^explain/insert/$', 'explain.views.insert'),

    # Examples:
    # url(r'^$', 'meme_expect.views.home', name='home'),
    # url(r'^meme_expect/', include('meme_expect.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
