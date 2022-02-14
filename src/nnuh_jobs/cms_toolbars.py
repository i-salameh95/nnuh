# -*- coding: utf-8 -*-
from aldryn_apphooks_config.utils import get_app_instance
from aldryn_translation_tools.utils import get_object_from_request
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.utils.translation import get_language_from_request, override
from django.utils.translation import ugettext_lazy as _
from aldryn_translation_tools.utils import (
    get_admin_url, get_object_from_request,
)
from nnuh_jobs.models import Job
from .cms_appconfig import JobsConfig


@toolbar_pool.register
class JobToolbar(CMSToolbar):
    supported_apps = (
        'nnuh_jobs',
    )
    watch_models = [Job,]

    def get_on_delete_redirect_url(self, job, language):
        with override(language):
            url = reverse(
                '{0}:job-list'.format(job.app_config.namespace))
        return url

    def __get_job_config(self):
        try:
            __, config = get_app_instance(self.request)
            if not isinstance(config, JobsConfig):
                # This is not the app_hook you are looking for.
                return None
        except ImproperlyConfigured:
            # There is no app_hook at all.
            return None
        return config

    def populate(self):
        config = self.__get_job_config()
        if not config:
            # Do nothing if there is no NewsBlog app_config to work with
            return

        user = getattr(self.request, 'user', None)
        try:
            view_name = self.request.resolver_match.view_name
        except AttributeError:
            view_name = None

        if user and view_name:
            language = get_language_from_request(self.request, check_path=True)

            # If we're on an Job detail page, then get the job
            if view_name == '{0}:job-detail'.format(config.namespace):
                job = get_object_from_request(Job, self.request)
            else:
                job = None

            menu = self.toolbar.get_or_create_menu('jobs_cms_integration',
                                                   config.get_app_title())

            change_config_perm = user.has_perm(
                'nnuh_jobs.change_jobconfig')
            add_config_perm = user.has_perm(
                'nnuh_jobs.add_jobconfig')
            config_perms = [change_config_perm, add_config_perm]

            change_job_perm = user.has_perm(
                'nnuh_jobs.change_job')
            delete_job_perm = user.has_perm(
                'nnuh_jobs.delete_job')
            add_job_perm = user.has_perm('nnuh_jobs.add_job')
            job_perms = [change_job_perm, add_job_perm,
                             delete_job_perm, ]

            if change_config_perm:
                url_args = {}
                if language:
                    url_args = {'language': language, }
                url = get_admin_url('nnuh_jobs_jobsconfig_change',
                                    [config.pk, ], **url_args)
                menu.add_modal_item(_('Configure addon'), url=url)

            if any(config_perms) and any(job_perms):
                menu.add_break()

            if change_job_perm:
                url_args = {}
                if config:
                    url_args = {'app_config__id__exact': config.pk}
                url = get_admin_url('nnuh_jobs_job_changelist',
                                    **url_args)
                menu.add_sideframe_item(_('Job list'), url=url)

            if add_job_perm:
                url_args = {'app_config': config.pk, 'owner': user.pk, }
                if language:
                    url_args.update({'language': language, })
                url = get_admin_url('nnuh_jobs_job_add', **url_args)
                menu.add_modal_item(_('Add new job'), url=url)

            if change_job_perm and job:
                url_args = {}
                if language:
                    url_args = {'language': language, }
                url = get_admin_url('nnuh_jobs_job_change',
                                    [job.pk, ], **url_args)
                menu.add_modal_item(_('Edit this job'), url=url,
                                    active=True)

            if delete_job_perm and job:
                redirect_url = self.get_on_delete_redirect_url(
                    job, language=language)
                url = get_admin_url('nnuh_jobs_job_delete',
                                    [job.pk, ])
                menu.add_modal_item(_('Delete this job'), url=url,
                                    on_close=redirect_url)
