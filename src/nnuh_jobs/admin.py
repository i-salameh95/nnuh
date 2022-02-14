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
from .models import Applier, Job



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
        }),
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
            'pagination_pages_visible', 'create_authors', 'template_prefix',
        )

admin.site.register(JobsConfig, JobConfigAdmin)

class ApplierAdmin(AllTranslationsMixin,
    PlaceholderAdminMixin,
    FrontendEditableAdminMixin,
    ModelAppHookConfig,
    TranslatableAdmin):

    list_display = ['__str__','sex','card_id','date_of_birth','email1','address','relations','relative_name',
    'relation_type','univ_study','univ_name','specialization','tel_no','mob_no']

    fieldsets = (
        (_('Personal Info'), {
            'fields': (
                'first_name',
                'second_name',
                'third_name',
                'family',
                'sex',
                'date_of_birth',
                'card_id',
            )
        }),
        (_('Contact Info'), {
            'fields': (
                'address',
                'tel_no',
                'mob_no',
                'email',
            )
        }),
        (_('Relations'), {
            'fields': (
                'relations',
                'relative_name',
                'relation_type',
            )
        }),
        (_('Educational'), {
            'fields': (
                'univ_study',
                'univ_name',
                'specialization',
                'country_grad',
                'year_grad',
                'grad_avg',
                'experience_years',
                'exp_sum',
                'tawjihi_branch',
                'tawjihi_country',
                'tawjihi_avg',
            )
        }),
    )
    
admin.site.register(Applier, ApplierAdmin)
