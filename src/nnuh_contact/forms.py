from cms.models import CMSPlugin
from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Field

from nnuh_contact.models import ContactMessage


class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactMessage
        fields = '__all__'

    def __init__(self, **kwargs):
        super(ContactForm, self).__init__(**kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.include_media = False
        self.helper.layout = Layout(
            # Div(
            Field('name', placeholder=_('Full Name')),
            Field('phone', placeholder=_('Phone/Mobile')),
            Field('email', placeholder=_('Email Address')),
            # Field('birth_date', placeholder=_('Birth Date')),
            Field('message', placeholder=_('Message')),
            #     css_class='large-icons-wrapper'
            # )
        )


