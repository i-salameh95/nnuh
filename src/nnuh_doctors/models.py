# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from cms.models import Page, PlaceholderField
from django.db import models
from django.urls import NoReverseMatch, reverse
from django.utils.translation import override, ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.utils.i18n import get_current_language, get_default_language

from aldryn_common.admin_fields.sortedm2m import SortedM2MModelField
from aldryn_translation_tools.models import TranslatedAutoSlugifyMixin, TranslationHelperMixin
from filer.fields.image import FilerImageField
from parler.models import TranslatableModel, TranslatedFields
from six import text_type

from .utils import get_additional_styles


try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse


class Section(TranslationHelperMixin, TranslatedAutoSlugifyMixin, TranslatableModel):
    slug_source_field_name = 'name'
    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=255,
                              help_text=_("Provide this section's title.")),
        slug=models.SlugField(
            _('slug'), max_length=255, default='',
            blank=True,
            help_text=_("Leave blank to auto-generate a unique slug.")),
    )
    page = models.ForeignKey(
        Page,
        verbose_name=_('Internal link'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('If provided, overrides the external link.'),
    )

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return self.safe_translation_getter(
            'title', default=_('Section: {0}').format(self.pk))

    def get_absolute_url(self, language=None):
        if not language:
            language = get_current_language() or get_default_language()
        return self.page.get_absolute_url(language=language)


class Doctor(TranslationHelperMixin, TranslatedAutoSlugifyMixin,
             TranslatableModel):
    slug_source_field_name = 'name'

    translations = TranslatedFields(
        name=models.CharField(
            _('name'), max_length=255, blank=False,
            default='', help_text=_("Provide this person's name.")),
        slug=models.SlugField(
            _('unique slug'), max_length=255, blank=True,
            default='',
            help_text=_("Leave blank to auto-generate a unique slug.")),
        speciality=models.CharField(_('speciality'), max_length=255),
        sub_speciality=models.CharField(_('sub speciality'), max_length=255, blank=True),
        function=models.CharField(_('role'), max_length=255, blank=True, default=''),
        clinic_time = models.CharField(_('clinic_time'), null=True, blank=True, max_length=255)
    )

    phone = models.CharField(
        verbose_name=_('phone'), null=True, blank=True, max_length=100)
    mobile = models.CharField(
        verbose_name=_('mobile'), null=True, blank=True, max_length=100)
    email = models.EmailField(
        verbose_name=_("email"), blank=True, default='')
    website = models.URLField(
        verbose_name=_('website'), null=True, blank=True)
    section = models.ForeignKey(
        Section, verbose_name=_('Section'), related_name='doctors', null=True, blank=True, on_delete=models.SET_NULL)
    visual = FilerImageField(
        null=True, blank=True, default=None, on_delete=models.SET_NULL)
    clinic_phone = models.CharField(_('clinic_phone'), null=True, blank=True, max_length=100)
    facebook = models.URLField(
        verbose_name=_('Facebook'), blank=True)
    twitter = models.URLField(
        verbose_name=_('Twitter'), blank=True)
    linkedin = models.URLField(
        verbose_name=_('LinkedIn'), blank=True)


    content = PlaceholderField('doctor_content', related_name='doctor_content')
    content_bottom = PlaceholderField('doctor_content_bottom', related_name='doctor_content_bottom')
    sidebar = PlaceholderField('doctor_sidebar', related_name='doctor_sidebar')
    sidebar_bottom = PlaceholderField('doctor_sidebar_bottom', related_name='doctor_sidebar_bottom')


    class Meta:
        verbose_name = _('Doctor')
        verbose_name_plural = _('Doctors')

    def __str__(self):
        pkstr = str(self.pk)
        name = self.safe_translation_getter(
            'name',
            default='',
            any_language=True
        ).strip()
        return name if len(name) > 0 else pkstr

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
            # do not fail with 500 error so that if detail view can't be
            # resolved we still can use plugins.
            try:
                url = reverse('nnuh_doctors:doctor-detail', kwargs=kwargs)
            except NoReverseMatch:
                url = ''
        return url


class Appointment(models.Model):
    section = models.ForeignKey(
        Section, verbose_name=_('Section'), related_name='appointments', null=True, blank=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        Doctor, verbose_name=_('Doctor'), related_name='appointments', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name=_('Full Name'), max_length=255)
    phone = models.CharField(
        verbose_name=_('Phone/Mobile'), max_length=255)
    email = models.CharField(
        verbose_name=_('Email Address'), max_length=255, blank=True)
    birth_date = models.CharField(
        verbose_name=_('Birth Date'), max_length=255, blank=True)
    message = models.TextField(
        verbose_name=_('Message'), blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Appointment')
        verbose_name_plural = _('Appointments')
        ordering = ['-created_at']

    def __str__(self):
        return '{} ({})'.format(self.name, self.doctor)


class BaseDoctorsPlugin(CMSPlugin):

    STYLE_CHOICES = [
        ('standard', _('Standard')),
        ('feature', _('Feature')),
        ('carousel', _('Carousel')),
    ] + get_additional_styles()

    style = models.CharField(
        _('Style'), choices=STYLE_CHOICES,
        default=STYLE_CHOICES[0][0], max_length=50)

    doctors = SortedM2MModelField(
        Doctor, blank=True,
        help_text=_('Select and arrange specific doctors, or, leave blank to '
                    'select all.')
    )

    # Add an app namespace to related_name to avoid field name clashes
    # with any other plugins that have a field with the same name as the
    # lowercase of the class name of this model.
    # https://github.com/divio/django-cms/issues/5030
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='%(app_label)s_%(class)s',
        parent_link=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    def copy_relations(self, oldinstance):
        self.doctors.set(oldinstance.doctors.all())

    def get_selected_doctors(self):
        return self.doctors.select_related('visual')

    def __str__(self):
        return text_type(self.pk)


class DoctorsPlugin(BaseDoctorsPlugin):

    show_links = models.BooleanField(
        verbose_name=_('Show links to Detail Page'), default=False)

    class Meta:
        abstract = False
