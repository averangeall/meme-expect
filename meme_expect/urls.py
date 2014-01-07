from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'reasonable.views.show'),
    url(r'^init/$', 'turker.views.init'),
    url(r'^fill/$', 'turker.views.fill'),
    url(r'^show/$', 'turker.views.show'),

    url(r'^ocr/$', 'ocr.views.write'),
    url(r'^insert/$', 'ocr.views.insert'),

    url(r'^browse/$', 'browse.views.every'),
    url(r'^browse/(?P<template_name>.+)$', 'browse.views.single'),

    url(r'^reasonable/$', 'reasonable.views.show'),

    # Examples:
    # url(r'^$', 'meme_expect.views.home', name='home'),
    # url(r'^meme_expect/', include('meme_expect.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
