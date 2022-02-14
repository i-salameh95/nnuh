# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_apphooks_config.models import AppHookConfig
from cms.models.fields import PlaceholderField
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from parler.models import TranslatableModel, TranslatedFields

TEMPLATE_PREFIX_CHOICES = getattr(
    settings, 'ALDRYN_NEWSBLOG_TEMPLATE_PREFIXES', [])

class JobsConfig(TranslatableModel, AppHookConfig):

    translations = TranslatedFields(
        app_title=  models.CharField(_('name'), max_length=234),
    )
    
    paginate_by = models.PositiveIntegerField(
        _('Paginate size'),
        blank=False,
        default=5,
        help_text=_('When paginating list views, how many articles per page?'),
    )
    pagination_pages_start = models.PositiveIntegerField(
        _('Pagination pages start'),
        blank=False,
        default=10,
        help_text=_('When paginating list views, after how many pages '
                    'should we start grouping the page numbers.'),
    )
    pagination_pages_visible = models.PositiveIntegerField(
        _('Pagination pages visible'),
        blank=False,
        default=4,
        help_text=_('When grouping page numbers, this determines how many '
                    'pages are visible on each side of the active page.'),
    )

    create_authors = models.BooleanField(
        _('Auto-create authors?'),
        default=True,
        help_text=_('Automatically create authors from logged-in user?'),
    )

    template_prefix = models.CharField(
        max_length=20,
        null=True, blank=True,
        choices=TEMPLATE_PREFIX_CHOICES,
        verbose_name=_("Prefix for template dirs")
    )

    def get_app_title(self):
        return getattr(self, 'app_title', _('untitled'))

    class Meta:
        verbose_name = _('NNUH Jobs configuration')
        verbose_name_plural = _('NNUH Jobs configurations')

    def __str__(self):
        return self.safe_translation_getter('app_title', any_language = True)
