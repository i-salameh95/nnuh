# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_newsblog.utils import get_plugin_index_data
from cms.models import CMSPlugin
from django.conf import settings

from aldryn_search.utils import get_index_base, strip_tags, clean_join
from django.utils.translation import gettext

from .models import Doctor


class DoctorsIndex(get_index_base()):
    haystack_use_for_indexing = getattr(settings, "NNUH_DOCTORS_SEARCH", True)

    INDEX_TITLE = True

    def get_title(self, obj):
        return obj.name

    # def get_description(self, obj):
    #     return gettext('NNUH Doctor')

    def get_index_kwargs(self, language):
        return {'translations__language_code': language}

    def get_index_queryset(self, language):
        return super(DoctorsIndex, self).get_index_queryset(language).language(language)
        # return self.get_model().objects.active_translations(
        #     language_code=language).translated(language)

    def get_model(self):
        return Doctor

    def get_search_data(self, obj, language, request):
        text_bits = []
        text_bits.append(obj.name)

        if obj.speciality:
            text_bits.append(obj.speciality)

        if obj.sub_speciality:
            text_bits.append(obj.sub_speciality)

        if obj.function:
            text_bits.append(obj.function)

        if obj.phone:
            text_bits.append(obj.phone)

        if obj.mobile:
            text_bits.append(obj.mobile)

        if obj.website:
            text_bits.append(obj.website)

        if obj.email:
            text_bits.append(obj.email)

        if obj.section:
            text_bits.append(obj.section.title)

        placeholders = [obj.content, obj.content_bottom, obj.sidebar, obj.sidebar_bottom]
        plugins = CMSPlugin.objects.filter(language=language).filter(placeholder__in=placeholders)
        for base_plugin in plugins:
            plugin_text_content = self.get_plugin_search_text(base_plugin, request)
            text_bits.append(plugin_text_content)

        return clean_join(' ', text_bits)

    def get_plugin_search_text(self, base_plugin, request):
        plugin_content_bits = get_plugin_index_data(base_plugin, request)
        return clean_join(' ', plugin_content_bits)

