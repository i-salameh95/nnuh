from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Field

from nnuh_doctors.models import Appointment


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        exclude = ['section']
        widgets = {
            'doctor': forms.HiddenInput()
        }

    def __init__(self, **kwargs):
        super(AppointmentForm, self).__init__(**kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.include_media = False
        self.helper.layout = Layout(
            'doctor',
            Field('name', placeholder=_('Full Name')),
            Field('phone', placeholder=_('Phone/Mobile')),
            Field('email', placeholder=_('Email Address')),
            Field('birth_date', placeholder=_('Birth Date')),
            Field('message', placeholder=_('Message'))
        )


class GeneralAppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        exclude = ['doctor']

    def __init__(self, **kwargs):
        super(GeneralAppointmentForm, self).__init__(**kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.include_media = False
        self.helper.layout = Layout(
            Field('section', placeholder=_('Section')),
            Field('name', placeholder=_('Full Name')),
            Field('phone', placeholder=_('Phone/Mobile')),
            Field('email', placeholder=_('Email Address')),
            Field('birth_date', placeholder=_('Birth Date')),
            Field('message', placeholder=_('Message'))
        )

