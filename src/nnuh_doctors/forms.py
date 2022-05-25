from pickle import FALSE
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django import forms
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2Widget

from nnuh_doctors.models import Appointment, Doctor, Section


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

class NnuhDoctorSectionSearchForm(forms.Form):

    doctor_type = forms.ModelChoiceField(queryset= Doctor.objects.all(), empty_label=_('Search'), widget=Select2Widget(attrs={'width': '100%'})) 
    section_type = forms.ModelChoiceField(queryset= Section.objects.all(),empty_label=_('Choose'), widget=Select2Widget(attrs={'width': '100%'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor_type'].label = _('search by name')
        self.fields['section_type'].label = _('Speciality')
        
        self.fields['doctor_type'].required = False
        self.fields['section_type'].required = False
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.include_media = False
        self.helper.layout = Layout(
            Div(
                Div(
                    Div('doctor_type', css_class='form-group col-md-6'),
                    Div('section_type', css_class='form-group col-md-3'),
                    Div(Submit('search',_('Search')), css_class='col-md-3'),
                    css_class='row flex-grow-1 align-items-center'
                ),
                css_class='d-flex justify-content-between align-items-center'
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        doctor_type = cleaned_data.get('doctor_type')
        section_type = cleaned_data.get('section_type')

        if doctor_type and section_type:
            raise forms.ValidationError(
                _("please use one filter for search")
            )
