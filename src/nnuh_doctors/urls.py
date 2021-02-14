# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url

from nnuh_doctors.views import DoctorDetailView, DoctorListView


urlpatterns = [
    # url(r'^section/(?P<pk>[0-9]+)/$',
    #     SectionDetailView.as_view(), name='section-detail'),
    # url(r'^section/(?P<slug>[A-Za-z0-9_\-]+)/$',
    #     SectionDetailView.as_view(), name='section-detail'),

    url(r'^(?P<pk>[0-9]+)/$',
        DoctorDetailView.as_view(), name='doctor-detail'),
    url(r'^(?P<slug>[A-Za-z0-9_\-]+)/$',
        DoctorDetailView.as_view(), name='doctor-detail'),

    url(r'^$',
        DoctorListView.as_view(), name='doctor-list'),

]
