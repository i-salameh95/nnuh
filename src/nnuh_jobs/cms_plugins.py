# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from aldryn_forms.cms_plugins import BaseTextField



class DateField(BaseTextField):
    name = _('Date Field')
    form_field_widget_input_type = 'date'

plugin_pool.register_plugin(DateField)


