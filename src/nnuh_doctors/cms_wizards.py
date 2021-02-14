# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.urls import NoReverseMatch, reverse
from django.utils.translation import ugettext_lazy as _

from cms.wizards.forms import BaseFormMixin
from cms.wizards.wizard_base import Wizard
from cms.wizards.wizard_pool import wizard_pool

from parler.forms import TranslatableModelForm

from .models import Section, Doctor


def has_published_apphook():
    """
    Returns a list of app_configs that are attached to a published page.
    """
    try:
        reverse('nnuh_doctors:doctor-list')
        return True
    except NoReverseMatch:
        pass
    return False


class BaseDoctorsWizard(Wizard):
    """
    Only return a success URL if we can actually use it.
    """
    def get_success_url(self, **kwargs):
        if has_published_apphook():
            return super(BaseDoctorsWizard, self).get_success_url(**kwargs)
        else:
            return None


class DoctorsDoctorWizard(BaseDoctorsWizard):

    def user_has_add_permission(self, user, **kwargs):
        """
        Return True if the current user has permission to add a doctor.
        :param user: The current user
        :param kwargs: Ignored here
        :return: True if user has add permission, else False
        """
        if user.is_superuser or user.has_perm("nnuh_doctors.add_doctor"):
            return True
        return False


class DoctorsSectionWizard(BaseDoctorsWizard):

    def user_has_add_permission(self, user, **kwargs):
        """
        Return True if the current user has permission to add a section.
        :param user: The current user
        :param kwargs: Ignored here
        :return: True if user has add permission, else False
        """
        if user.is_superuser or user.has_perm("nnuh_doctors.add_section"):
            return True
        return False


class CreateDoctorsDoctorForm(BaseFormMixin, TranslatableModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'section', 'speciality', 'sub_speciality', 'function',
                  'phone', 'mobile', 'email', 'website', 'facebook', 'linkedin', 'twitter']


class CreateDoctorsSectionForm(BaseFormMixin, TranslatableModelForm):
    class Meta:
        model = Section
        fields = ['title', 'page']


doctors_doctor_wizard = DoctorsDoctorWizard(
    title=_('New doctor'),
    weight=300,
    form=CreateDoctorsDoctorForm,
    description=_("Create a new doctor.")
)

wizard_pool.register(doctors_doctor_wizard)


doctors_section_wizard = DoctorsSectionWizard(
    title=_('New section'),
    weight=300,
    form=CreateDoctorsSectionForm,
    description=_("Create a new section.")
)

# Disabling the section wizard by default. To enable, create a file
# cms_wizards.py in your project and add the following lines:

# from cms.wizards.wizard_pool import wizard_pool
# from nnuh_doctors.cms_wizards import doctors_section_wizard
#
#  wizard_pool.register(doctors_section_wizard)
