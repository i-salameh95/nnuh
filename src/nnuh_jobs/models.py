# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from aldryn_apphooks_config.fields import AppHookConfigField
from aldryn_people.models import Person
from aldryn_translation_tools.models import (TranslatedAutoSlugifyMixin,
                                             TranslationHelperMixin)
from cms.models.fields import PlaceholderField
from cms.utils.i18n import get_current_language
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify  # new
from django.template.defaultfilters import filesizeformat
from django.urls import NoReverseMatch, reverse
from django.utils.timezone import now
from django.utils.translation import override
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField
from parler.models import TranslatableModel, TranslatedFields

from .cms_appconfig import JobsConfig
from .managers import RelatedManager


# Create your models here.
class Job(TranslationHelperMixin, TranslatedAutoSlugifyMixin,
             TranslatableModel):

    slug_source_field_name = 'title'

    translations = TranslatedFields(
        title = models.CharField(
            _('title'), max_length=500, blank=False,
            default='', help_text=_("Provide this job's title.")),
        slug = models.SlugField(
            verbose_name=_('slug'),
            max_length=255,
            db_index=True,
            blank=True,
            help_text=_(
                'Used in the URL. If changed, the URL will change. '
                'Clear it to have it re-created automatically.'),
        ),
    )

    publishing_date = models.DateTimeField(_('publishing date'),
                                           default=now)
    deadline_date = models.DateTimeField(_('deadline date'),
                                           default=now)
    is_active = models.BooleanField(_('active?'), default=True)
    can_apply = models.BooleanField(_('viewer can apply for the job?'), default=True)

    featured_image = FilerImageField(
        verbose_name=_('featured image'),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    author = models.ForeignKey(
        Person,
        null=True,
        blank=True,
        verbose_name=_('author'),
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('owner'),
        on_delete=models.CASCADE,
    )

    content = PlaceholderField('Job_Description', related_name='job_content')
    apply_form = PlaceholderField('Job_Form', related_name='apply_form')

    app_config = AppHookConfigField(
        JobsConfig,
        verbose_name=_('NNUH Jobs Configuration'),
        help_text='',
    )
   
    objects = RelatedManager()

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')
        ordering = ['-publishing_date']
    
    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)

    def get_absolute_url(self, language=None):
        if not language:
            language = get_current_language()
        slug, language = self.known_translation_getter(
            'slug', None, language_code=language)
        if slug:
            kwargs = {'slug': slug}
        else:
            kwargs = {'pk': self.pk}
        with override(language):
            try:
                url = reverse('nnuh_jobs:job-detail', kwargs=kwargs)
            except NoReverseMatch:
                url = ''
            url = reverse('nnuh_jobs:job-detail', kwargs=kwargs)
        return url

    @property
    def get_active(self):
        return all([
            self.is_active,
            self.publishing_date is None or self.publishing_date <= now(),
            self.deadline_date is None or self.deadline_date > now()
        ])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
