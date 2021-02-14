# -*- coding: utf-8 -*-
from django import template

from phonenumbers import PhoneNumberFormat, format_number, parse
from phonenumbers.phonenumberutil import NumberParseException


register = template.Library()


@register.simple_tag()
def get_autogen_reverse_id(page_id):
    return 'page_autogen_reverse_id__{}'.format(page_id)
