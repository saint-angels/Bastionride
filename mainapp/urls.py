# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('mainapp.views',

    url(r'^$', 'index', name='index'),
    url(r'^about/$', 'about', name='about'),
    url(r'^gallery/$', 'gallery', name='gallery'),
)
