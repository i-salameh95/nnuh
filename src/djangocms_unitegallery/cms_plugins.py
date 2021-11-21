# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import Gallery, CONFIG
from .admin import PhotoInline


class GalleryPlugin(CMSPluginBase):
    """
    The gallery plugin instance.
    """
    model = Gallery
    name = _('Gallery')
    module = _('Unite gallery')
    inlines = [PhotoInline, ]

    def get_render_template(self, context, instance, placeholder):
        try:
            import easy_thumbnails
            return 'djangocms_unitegallery/gallery.html'
        except ImportError:
            return 'djangocms_unitegallery/gallery.html'

    def render(self, context, instance, placeholder):
        context.update({
            'gallery': instance,
            'placeholder': placeholder,
            'CONFIG': CONFIG,
        })
        return context
        
plugin_pool.register_plugin(GalleryPlugin)
