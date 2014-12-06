# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include


urlpatterns = patterns('mainapp.views',

    url(r'^$', 'index', name='index'),
    url(r'^about/$', 'about', name='about'),
    url(r'^gallery/$', 'gallery', name='gallery'),
    url(r'^feedback/$', 'feedback', name='feedback'),
    url(r'^hitcount_image/$', 'hitcount_image', name='hitcount_image'),
)


urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)