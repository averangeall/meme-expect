from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'turker.views.expect'),
    url(r'^init/$', 'turker.views.init'),
    url(r'^fill/$', 'turker.views.fill'),
    url(r'^show/$', 'turker.views.show'),

    # Examples:
    # url(r'^$', 'meme_expect.views.home', name='home'),
    # url(r'^meme_expect/', include('meme_expect.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
