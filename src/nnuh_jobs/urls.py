# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url
from nnuh_jobs.views import JobDetail, JobList, ApplyJob

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$',
        JobDetail.as_view(), name='job-detail'),
    url(r'^(?P<slug>[A-Za-z0-9_\-]+)/$',
       JobDetail.as_view(), name='job-detail'),
    url(r'^$',
        JobList.as_view(), name='job-list'),
    url(r'^(?P<slug>[A-Za-z0-9_\-]+)/apply-job/(?P<jobId>[0-9]+)$', 
        ApplyJob.as_view(),name='apply-job-form')
]
