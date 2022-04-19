from __future__ import unicode_literals

from aldryn_apphooks_config.admin import BaseAppHookConfig, ModelAppHookConfig
from aldryn_people.models import Person
from aldryn_translation_tools.admin import AllTranslationsMixin
from cms.admin.placeholderadmin import (FrontendEditableAdminMixin,
                                        PlaceholderAdminMixin)
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from parler.admin import TranslatableAdmin
from nnuh_jobs.cms_appconfig import JobsConfig
from .models import  Job



class JobAdmin( AllTranslationsMixin,
    PlaceholderAdminMixin,
    FrontendEditableAdminMixin,
    ModelAppHookConfig,
    TranslatableAdmin):

    list_display = ['__str__','publishing_date', 'deadline_date','is_active','can_apply','author']
    list_filter = ['deadline_date' , 'publishing_date' ]
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slug',
                'author',
            )
        }),
        (_('Publication Period'), {
            'fields': ('publishing_date', 'deadline_date')
        }),
        (_('Options'), {
            'classes': ('collapse',),
            'fields': (
                'is_active',
                'can_apply',
            )
        }),
        (_('Advanced Settings'), {
            'classes': ('collapse',),
            'fields': (
                'owner',
                'featured_image',
                'app_config',
            )
        })
    )
   
    def add_view(self, request, *args, **kwargs):
        data = request.GET.copy()
        try:
            person = Person.objects.get(user=request.user)
            data['author'] = person.pk
            request.GET = data
        except Person.DoesNotExist:
            pass

        data['owner'] = request.user.pk
        request.GET = data
        return super(JobAdmin, self).add_view(request, *args, **kwargs)

admin.site.register(Job, JobAdmin)


class JobConfigAdmin(
    AllTranslationsMixin,
    PlaceholderAdminMixin,
    BaseAppHookConfig,
    TranslatableAdmin
):
    def get_config_fields(self):
        return (
            'app_title', 'paginate_by', 'pagination_pages_start',
            'pagination_pages_visible', 'create_authors')

admin.site.register(JobsConfig, JobConfigAdmin)