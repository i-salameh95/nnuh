# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from cms.models import CMSPlugin
from aldryn_apphooks_config.fields import AppHookConfigField
from aldryn_people.models import Person
from aldryn_translation_tools.models import (TranslatedAutoSlugifyMixin,
                                             TranslationHelperMixin)
from cms.models.fields import PlaceholderField
from cms.utils.i18n import get_current_language
from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify  # new
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import override
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField
from parler.models import TranslatableModel, TranslatedFields
from .managers import RelatedManager
from .cms_appconfig import JobsConfig


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
    
    # @property
    # def published(self):
    #     """
    #     Returns True only if the article (is_published == True) AND has a
    #     published_date that has passed.
    #     """
    #     return self.is_published and self.publishing_date <= now() 
    
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


class Applier(TranslationHelperMixin, TranslatedAutoSlugifyMixin,
            TranslatableModel):
    
    MALE = 'male'
    FEMALE = 'female'
    SALUTATION_CHOICES = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    )

    BACHELOR = 'Bachelor' 
    MASTER = 'Master' 
    DOCTOR = 'Doctoral'
    STUDY_CATEGORY_CHOISES = (
        (BACHELOR, _('Bachelor')),
        (MASTER, _('Master')),
        (DOCTOR, _('Doctoral')),
    )

    LESS_THAN_YEAR = 'less than year'
    MORE_THAN_10_YEARS= 'more than 10 years'
    EXP_YEARS = (
        (LESS_THAN_YEAR, 'LESS_THAN_YEAR'),(1,'1'), (2,'2'), (3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10'),(MORE_THAN_10_YEARS,'10+')
    )

    SCIENTIFIC = 'Scientific'
    INDUSTRIAL = 'Industrial'
    COMMERCIAL = 'Commercial'
    LITERATURE = 'Literature'
    TAWJIHI_BRANCH = (
        (SCIENTIFIC, _('Scientific')),
        (LITERATURE, _('Literature')),
        (INDUSTRIAL, _('Industrial')),
        (COMMERCIAL, _('Commercial'))
    )

    translations = TranslatedFields(
        first_name = models.CharField(_('first name'), null=False,max_length=20),
        second_name = models.CharField(_('second name'), null=False,max_length=20),
        third_name = models.CharField(_('third_name'),null=True,max_length=20),
        family = models.CharField(_('last name'),null=False,max_length=20),
        address = models.TextField(_('address'),null=False),
        relations = models.BooleanField(_('realtion'),default = False),
        relative_name = models.CharField(_('relative name'), null=True, max_length=40),
        relation_type = models.CharField(_('relation type'), null=True, max_length=20),
        univ_study = models.CharField(_('University Study'), choices= STUDY_CATEGORY_CHOISES, max_length=20, null=False),
        univ_name = models.CharField(_('University Name'), max_length= 50, null=False),
        specialization= models.CharField(_('specialization'), max_length=50, null=False),
    )

    tel_no = models.CharField(_('Telephone No.'),max_length=20, null=False)
    mob_no = models.CharField(_('Mobile No.'),max_length=20, null=False)
    email1 = models.EmailField(_('Email'), max_length=255, null=False)
    verify_email = models.EmailField(_('Verify Email'), max_length=255, null=False)
    card_id = models.CharField(_('ID Number'), max_length=10, null=False)
    sex = models.CharField( verbose_name=_('Gender'), null=False, choices= SALUTATION_CHOICES, default= MALE, max_length= 10)
    date_of_birth = models.DateField(_('Birthday'), null=False)
    country_grad = models.CharField(_('Country Graduation'), null=False, max_length= 20)
    year_grad = models.CharField(_('Graduation Year'), max_length=4, null=False)
    grad_avg = models.CharField(_('Graduation Average'), max_length=5, null=False)
    experience_years = models.CharField(_('Experience Years'), choices=EXP_YEARS , null=False, max_length= 20)
    exp_sum = models.TextField(_('Experience Details'))
    tawjihi_branch = models.CharField(_('Tawjihi Branch'), choices=TAWJIHI_BRANCH, null=False, max_length= 20)
    tawjihi_avg = models.CharField(_('Tawjihi Average'),max_length=5, null=False)
    tawjihi_country = models.CharField(_('Tawjihi Country'),max_length=20, null=False)
    cv = PlaceholderField('Job_CV', related_name='Job_CV')
    tawjihi = PlaceholderField('Job_Tawjihi', related_name='Job_Tawjihi')
    certificate = PlaceholderField('Job_Certificate', related_name='Job_Certificate')
    master_cert= PlaceholderField('Job_Master', related_name='Job_Master')
    experience= PlaceholderField('Job_Expeience', related_name='Job_Expeience')


    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        full_name = ' '.join([self.first_name, self.family])
        return full_name.strip()
    
    def save(self, *args, **kwargs):
        if not self.pk:
            #
            # If using something like Celery, then this should be scheduled, not
            # executed in the request/response cycle.
            #
            try:
                self.send_notification_email()
            except:
                #
                # This is just a precaution, should there be an issue with the
                # emailing, we do not want this to prevent the new Contact
                # object from being saved.
                #
                pass
        super(Applier, self).save(*args, **kwargs)
    
class JobApplication(TranslationHelperMixin, TranslatedAutoSlugifyMixin,
             TranslatableModel):

    jobpost = models.ForeignKey(Job, on_delete=models.CASCADE, editable=False, related_name='Job', blank=True, null=True)
    applicant = models.ForeignKey(Applier, editable=False, on_delete=models.CASCADE, related_name='Applier')
    date_applied = models.DateTimeField(auto_now=False, auto_now_add=True)
