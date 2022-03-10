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

    list_display = ['__str__','publishing_date', 'deadline_date','is_active','can_apply','author',   'cv_option','tawjihi_option','certificate_option',
                'ID_option',
                'personal_photo_option',
                'work_cert_option',
                'org_cert_option',
                'recommendation_letters_option',
                'personal_statment_option',
                'marks_list_option',
                'insurance_doc_option'
            ]
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
        (_('Option Files to be added to Job Form'), {
            'classes': ('collapse',),
            'fields': (
                'cv_option',
                'tawjihi_option',
                'certificate_option',
                'ID_option',
                'personal_photo_option',
                'work_cert_option',
                'org_cert_option',
                'recommendation_letters_option',
                'personal_statment_option',
                'marks_list_option',
                'insurance_doc_option',
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

# class ApplierAdmin(admin.ModelAdmin):

#     list_display = ['__str__','sex','card_id_number','date_of_birth','email1','address','relations','relative_name',
#     'relation_type','tel_no','mob_no']

#     fieldsets = (
#         (_('Personal Info'), {
#             'fields': (
#                 'first_name',
#                 'second_name',
#                 'third_name',
#                 'family',
#                 'sex',
#                 'card_id_number',
#                 'date_of_birth',
#             )
#         }),
#         (_('Contact Info'), {
#             'fields': (
#                 'address',
#                 'tel_no',
#                 'mob_no',
#                 'email',
#                 'verify_email',
#             )
#         }),
#         (_('Relations'), {
#             'fields': (
#                 'relations',
#                 'relative_name',
#                 'relation_type',
#             )
#         })
#     )
    
# admin.site.register(Applier, ApplierAdmin)
