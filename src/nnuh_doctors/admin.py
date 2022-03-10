# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from cms.admin.placeholderadmin import PlaceholderAdminMixin

from aldryn_translation_tools.admin import AllTranslationsMixin
from parler.admin import TranslatableAdmin

from .models import Section, Doctor, Appointment


class DoctorAdmin(PlaceholderAdminMixin,
                  AllTranslationsMixin,
                  TranslatableAdmin):

    list_display = [
        '__str__', 'email', ]
    list_filter = ['section', ]
    search_fields = ('translations__name', 'email', 'translations__speciality',
                     'translations__sub_speciality', 'translations__function')
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'slug',
                'visual',
                'section',
                ('speciality', 'sub_speciality', ),
                'function',
                ('clinic_phone', 'clinic_time',)
            ),
        }),
        (_('Contact (untranslated)'), {
            'fields': (
                'phone', 'mobile', 'email', 'website', 
            ),
        }),
        (_('Social Media (untranslated)'), {
            'fields': (
                'facebook', 'twitter', 'linkedin',
            ),
        }),
    )


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('section', 'doctor', 'name', 'phone', 'email', 'birth_date', 'created_at', )
    list_display_links = ('name', )
    list_filter = ('section', 'doctor', )
    search_fields = ('section', 'doctor', 'name', )


class SectionAdmin(PlaceholderAdminMixin,
                 AllTranslationsMixin,
                 TranslatableAdmin):

    list_display = ['__str__', 'title', 'num_doctors', ]
    search_filter = ['translations__title']
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slug',
            ),
        }),
        (_('Link (untranslated)'), {
            'fields': (
                'page',
            )
        }),
    )

    def get_queryset(self, request):
        qs = super(SectionAdmin, self).get_queryset(request)
        qs = qs.annotate(doctors_count=Count('doctors'))
        return qs

    def num_doctors(self, obj):
        return obj.doctors_count
    num_doctors.short_description = _('# Doctor')
    num_doctors.admin_order_field = 'doctors_count'


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Appointment, AppointmentAdmin)
