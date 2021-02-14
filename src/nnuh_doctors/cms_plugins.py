# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from nnuh_doctors import DEFAULT_APP_NAMESPACE, models
from nnuh_doctors.forms import GeneralAppointmentForm

from .utils import get_valid_languages


NAMESPACE_ERROR = _(
    "Seems that there is no valid application hook for nnuh-doctors."
    "Links can't be rendered without an app hook."
)


class DoctorsPlugin(CMSPluginBase):

    TEMPLATE_NAME = 'nnuh_doctors/plugins/%s/doctors_list.html'
    module = 'NNUH'
    render_template = TEMPLATE_NAME % models.DoctorsPlugin.STYLE_CHOICES[0][0]
    name = _('Doctors list')
    model = models.DoctorsPlugin

    fieldsets = (
        (None, {
            'fields': (
                'style',
            ),
        }),
        (_('Doctors'), {
            'description': _('Select and arrange specific people, or leave '
                             'blank to use all.'),
            'fields': (
                'doctors',
            )
        }),
        (_('Options'), {
            'fields': (
                'show_links',
            )
        })
    )

    def render(self, context, instance, placeholder):
        doctors = instance.get_selected_doctors()
        if not doctors:
            doctors = models.Doctor.objects.all()
        valid_languages = get_valid_languages(
            DEFAULT_APP_NAMESPACE, instance.language, context['request'])
        doctors = doctors.translated(*valid_languages)
        if not valid_languages:
            context['namespace_error'] = NAMESPACE_ERROR
        self.render_template = self.TEMPLATE_NAME % instance.style

        context['instance'] = instance
        context['doctors'] = doctors

        return context



class GeneralAppointmentPlugin(CMSPluginBase):

    render_template = 'nnuh_doctors/plugins/general_appointment_form.html'
    module = 'NNUH'
    name = _('General Appointment Form')

    def render(self, context, instance, placeholder):
        request = context['request']
        if request.method == "POST":
            form = GeneralAppointmentForm(data=request.POST, files=request.FILES)
        else:
            form = GeneralAppointmentForm()
        if request.method == "POST" and form.is_valid():
            form.save()
            path = '{}?general-appointment-form-status=success#general_appointment_form'.format(request.path_info)
            setattr(request, 'nnuh_general_appointment_redirect_to', HttpResponseRedirect(path))
        if request.method == "GET" and request.GET.get('general-appointment-form-status', None) == 'success':
            context['message'] = _('Message has been received successfully.')
        context['instance'] = instance
        context['form'] = form
        return context


plugin_pool.register_plugin(DoctorsPlugin)
plugin_pool.register_plugin(GeneralAppointmentPlugin)
