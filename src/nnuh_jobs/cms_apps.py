# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_apphooks_config.app_base import CMSConfigApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from .cms_appconfig import JobsConfig


class JobsApp(CMSConfigApp):
    name = _('Jobs')
    app_name = 'nnuh_jobs'
    app_config = JobsConfig
    
    def get_urls(self, page=None, language=None, **kwargs):
        return ['nnuh_jobs.urls']

apphook_pool.register(JobsApp)
