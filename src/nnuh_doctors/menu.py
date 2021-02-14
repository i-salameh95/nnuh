# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.urls import NoReverseMatch
from django.utils.translation import get_language_from_request, ugettext as _

from cms.menu_bases import CMSAttachMenu

from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from .models import Section, Doctor


class DoctorMenu(CMSAttachMenu):
    """
    Provides an attachable menu of all people.
    """
    name = _('NNUH Doctors: Doctor Menu')

    def get_nodes(self, request):
        nodes = []
        language = get_language_from_request(request, check_path=True)
        doctors = (Doctor.objects.language(language)
                   .active_translations(language))

        for doctor in doctors:
            try:
                url = doctor.get_absolute_url(language=language)
            except NoReverseMatch:
                url = None
            if url:
                node = NavigationNode(
                    doctor.safe_translation_getter(
                        'name', default=_('doctor: {0}').format(doctor.pk),
                        language_code=language),
                    url,
                    doctor.pk,
                )
                nodes.append(node)
        return nodes


menu_pool.register_menu(DoctorMenu)


class SectionMenu(CMSAttachMenu):
    """
    Provides an attachable menu of all sections.
    """
    name = _('NNUH Doctors: Section Menu')

    def get_nodes(self, request):
        nodes = []
        language = get_language_from_request(request, check_path=True)
        sections = (Section.objects.language(language)
                               .active_translations(language))

        for section in sections:
            try:
                url = section.get_absolute_url(language=language)
            except NoReverseMatch:
                url = None
            if url:
                node = NavigationNode(
                    section.safe_translation_getter(
                        'title', default=_('section: {0}').format(section.pk),
                        language_code=language),
                    url,
                    section.pk,
                )
                nodes.append(node)
        return nodes


menu_pool.register_menu(SectionMenu)
