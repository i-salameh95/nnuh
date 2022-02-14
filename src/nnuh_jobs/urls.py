# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url
from nnuh_jobs.views import JobDetail, JobList, ApplyJobFormView

urlpatterns = [
    # url(r'^', JobList.as_view(), name='job-list'),
    # url(r'^(?P<slug>[^/]+)/$',
    #     JobDetail.as_view(), name='job-detail'),
    url(r'^(?P<pk>[0-9]+)/$',
        JobDetail.as_view(), name='job-detail'),
    url(r'^(?P<slug>[A-Za-z0-9_\-]+)/$',
       JobDetail.as_view(), name='job-detail'),
    url(r'^$',
        JobList.as_view(), name='job-list'),
    url(r'^apply-job/(?P<pk>[0-9]+)/$', ApplyJobFormView.as_view(),name='apply-job')
]
