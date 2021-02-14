# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from .models import ContactMessage


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at', )
    list_display_links = ('name', )
    search_fields = ('name', )


admin.site.register(ContactMessage, ContactMessageAdmin)
