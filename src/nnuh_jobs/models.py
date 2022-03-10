# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from aldryn_apphooks_config.fields import AppHookConfigField
from aldryn_people.models import Person
from aldryn_translation_tools.models import (TranslatedAutoSlugifyMixin,
                                             TranslationHelperMixin)
from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
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
# from forms_builder.forms.models import Form
from parler.models import TranslatableModel, TranslatedFields

from .cms_appconfig import JobsConfig
from .managers import RelatedManager


class RestrictedFileField(forms.FileField):
    """
    Same as FileField, but you can specify:
    * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
    * max_upload_size - a number indicating the maximum file size allowed for upload.
        2.5MB - 2621440
        5MB - 5242880
        10MB - 10485760
        20MB - 20971520
        50MB - 5242880
        100MB - 104857600
        250MB - 214958080
        500MB - 429916160
"""

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")

        super(RestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        file = super(RestrictedFileField, self).clean(data, initial)

        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise ValidationError(_('Please keep filesize under %s. Current filesize %s') % (
                        filesizeformat(self.max_upload_size), filesizeformat(file._size)))
            else:
                raise ValidationError(_('Filetype not supported.'))
        except AttributeError:
            pass

        return data

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

    ##boolean fields for files
    cv_option = models.BooleanField(_('CV file'), default=True )
    tawjihi_option = models.BooleanField(_('Tawjihi Certificate file'), default=True)
    certificate_option = models.BooleanField(_('BA University Certificate'), default=False)
    ID_option = models.BooleanField(_('Card ID option '), default=True)
    personal_photo_option = models.BooleanField(_('Personal Photo File'), default=False)
    work_cert_option = models.BooleanField(_('Work Certificate File'), default=True)
    org_cert_option = models.BooleanField(_('Org Certificate File'), default=True)
    recommendation_letters_option = models.BooleanField(_('Recommendation Letters File'), default=False)
    personal_statment_option = models.BooleanField(_('Personal Statement File'), default=False)
    marks_list_option = models.BooleanField(_('Marks_List'),default=False)
    insurance_doc_option = models.BooleanField(_('Insurance Doc'), default= False)

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


# class Applier(TranslationHelperMixin, TranslatedAutoSlugifyMixin,
#             TranslatableModel):
    
#     MALE = 'male'
#     FEMALE = 'female'
#     SALUTATION_CHOICES = (
#         (MALE, _('Male')),
#         (FEMALE, _('Female')),
#     )
#     BOOL_CHOICES = ((True, _('Yes')), (False, _('No')))
#     #################################################### Personal Information #######################################
#     first_name = models.CharField(_('first name'), null=False,max_length=20)
#     second_name = models.CharField(_('second name'), null=False,max_length=20)
#     third_name = models.CharField(_('third_name'),null=True,max_length=20)
#     family = models.CharField(_('last name'),null=False,max_length=20)
#     sex = models.CharField( verbose_name=_('Gender'), null=False, choices= SALUTATION_CHOICES, default= MALE, max_length= 10)
#     card_id_number = models.CharField(_('ID Number'), max_length=10, null=False)
#     date_of_birth = models.DateField(_('Birthday'), null=False)

#     #################################################### Contact Info ##################################################
#     tel_no = models.CharField(_('Telephone No.'),max_length=20, null=False)
#     mob_no = models.CharField(_('Mobile No.'),max_length=20, null=False)
#     email1 = models.EmailField(_('Email'), max_length=255, null=False)
#     verify_email = models.EmailField(_('Verify Email'), max_length=255, null=False)
#     address = models.TextField(_('address'), null=False)

#     #################################################### Relations ####################################################
#     relations = models.BooleanField(_('realtion'),choices=BOOL_CHOICES, default= False)
#     relative_name = models.CharField(_('relative name'), null=True, max_length=40, blank= True)
#     relation_type = models.CharField(_('relation type'), null=True, max_length=20, blank=True)

#     ##############################################################################files#################################
    
#     cv = models.FileField(
#         verbose_name=_('CV'),
#         null=True,
#         default= None)
#     tawjihi = models.FileField(
#         verbose_name=_('Personal Photo'),
#         null=True,
#         default= None
#     )
#     certificate = models.FileField(_('BA University Certificate'),  null=True,default= None)
#     card_ID_file = models.FileField(_('Card ID file'),   null=True,default= None)
#     personal_photo = models.FileField(_('Personal Photo File'),   null=True,default= None)
#     work_cert = models.FileField(_('Work Certificate File'),   null=True,default= None)
#     org_cert = models.FileField(_('Org Certificate File'),   null=True,default= None)
#     recommendation_letters = models.FileField(_('Recommendation Letters File'),   null=True,default= None)
#     personal_statment = models.FileField(_('Personal Statement File'),   null=True,default= None)
#     marks_list = models.FileField(_('Marks_List'),  null=True,default= None)
#     insurance_doc = models.FileField(_('Insurance Doc'),   null=True,default= None)



#     def __str__(self):
#         return self.get_full_name()

#     def get_full_name(self):
#         full_name = ' '.join([self.first_name, self.family])
#         return full_name.strip()


# class ApplierForm(CMSPlugin):
#     form = models.ForeignKey(Form, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.form.title
   
# class JobApplication(TranslationHelperMixin, TranslatedAutoSlugifyMixin,
#              TranslatableModel):

#     jobpost = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='Job')
#     applicant = models.ForeignKey(ApplierForm, on_delete=models.CASCADE, related_name='ApplierForm')
#     date_applied = models.DateTimeField(auto_now=False, auto_now_add=True)
