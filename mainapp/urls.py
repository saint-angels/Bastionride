# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include


urlpatterns = patterns('mainapp.views',

    url(r'^$', 'index', name='index'),
    url(r'^about/$', 'about', name='about'),
    url(r'^gallery/$', 'gallery', name='gallery'),
    url(r'^feedback/$', 'feedback', name='feedback'),
    url(r'^hitcount_image/$', 'hitcount_image', name='hitcount_image'),
    url(r'^polls/$', 'polls', name='polls'),
    url(r'^polls/vote/(?P<question_id>[0-9]+)$', 'vote', name='vote'),
    url(r'^polls/question_info_image/(?P<question_id>[0-9]+)$', 'question_info_image', name='question_info_image'),
)


urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)