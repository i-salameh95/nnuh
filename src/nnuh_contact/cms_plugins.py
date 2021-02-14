# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from nnuh_contact.forms import ContactForm
from nnuh_contact.models import ContactFormPluginModel, Recipient


class RecipientInline(admin.TabularInline):
    model = Recipient

class ContactFormPlugin(CMSPluginBase):


    render_template = 'nnuh_contact/plugins/contact_form.html'
    module = 'NNUH'
    name = _('Contact Us')
    model = ContactFormPluginModel
    inlines = (RecipientInline,)

    def render(self, context, instance, placeholder):
        request = context['request']
        if request.method == "POST":
            form = ContactForm(data=request.POST, files=request.FILES)
        else:
            form = ContactForm()
        if request.method == "POST" and form.is_valid():
            form.save()
            print("^" * 80)
            print("set attribute {}".format(request.path_info))
            path = '{}?contact-form-status=success#contact_us_form'.format(request.path_info)
            setattr(request, 'nnuh_contact_redirect_to', HttpResponseRedirect(path))
        if request.method == "GET" and request.GET.get('contact-form-status', None) == 'success':
            context['message'] = _('Message has been received successfully.')
        context['instance'] = instance
        context['form'] = form
        return context


plugin_pool.register_plugin(ContactFormPlugin)
