# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_apphooks_config.mixins import AppConfigMixin
from aldryn_newsblog.compat import toolbar_edit_mode_active
from aldryn_newsblog.utils.utilities import get_valid_languages_from_request
from cms.models.pagemodel import Page
from django.shortcuts import get_object_or_404
from django.utils import translation
from django.views.generic import DetailView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from menus.utils import set_language_changer
from parler.views import TranslatableSlugMixin, ViewUrlMixin

from .forms import ApplyJobForm
from .models import Job,Applier


class EditModeMixin(object):
    """
    A mixin which sets the property 'edit_mode' with the truth value for
    whether a user is logged-into the CMS and is in edit-mode.
    """
    edit_mode = False

    def dispatch(self, request, *args, **kwargs):
        self.edit_mode = (
            self.request.toolbar and toolbar_edit_mode_active(self.request))
        return super(EditModeMixin, self).dispatch(request, *args, **kwargs)


class PreviewModeMixin(EditModeMixin):
    """
    If content editor is logged-in, show all active articles. Otherwise, only the
    published articles should be returned.
    """
    def get_queryset(self):
        qs = super(PreviewModeMixin, self).get_queryset()
        # check if user can see unpublished items. this will allow to switch
        # to edit mode instead of 404 on article detail page. CMS handles the
        # permissions.
        user = self.request.user
        user_can_edit = user.is_staff or user.is_superuser
        if not (self.edit_mode or user_can_edit):
            qs = qs.active() #################### qs.published()
        language = translation.get_language()
        qs = qs.active_translations(language).namespace(self.namespace)
        return qs


class AppHookCheckMixin(object):

    def dispatch(self, request, *args, **kwargs):
        self.valid_languages = get_valid_languages_from_request(
            self.namespace, request)
        return super(AppHookCheckMixin, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        # filter available objects to contain only resolvable for current
        # language. IMPORTANT: after .translated - we cannot use .filter
        # on translated fields (parler/django limitation).
        # if your mixin contains filtering after super call - please place it
        # after this mixin.
        qs = super(AppHookCheckMixin, self).get_queryset()
        return qs.translated(*self.valid_languages)


def get_language(request):
    lang = getattr(request, 'LANGUAGE_CODE', None)
    if lang is None:
        lang = get_language_from_request(request, check_path=True)
    return lang


class LanguageChangerMixin(object):
    """
    Convenience mixin that adds CMS Language Changer support.
    """
    def get(self, request, *args, **kwargs):
        if not hasattr(self, 'object'):
            self.object = self.get_object()
        set_language_changer(request, self.object.get_absolute_url)
        return super(LanguageChangerMixin, self).get(request, *args, **kwargs)


class AllowPKsTooMixin(object):
    def get_object(self, queryset=None):
        """
        Bypass TranslatableSlugMixin if we are using PKs. You would only use
        this if you have a view that supports accessing the object by pk or
        by its translatable slug.

        NOTE: This should only be used on DetailViews and this mixin MUST be
        placed to the left of TranslatableSlugMixin. In fact, for best results,
        declare your view like this:

            MyView(…, AllowPKsTooMixin, TranslatableSlugMixin, DetailView):
        """
        if self.pk_url_kwarg in self.kwargs:
            return super(DetailView, self).get_object(queryset)

        # OK, just let Parler have its way with it.
        return super(AllowPKsTooMixin, self).get_object(queryset)


class JobDetail(AppConfigMixin, AppHookCheckMixin, PreviewModeMixin,
                    TranslatableSlugMixin, DetailView):
    model = Job
    slug_field = 'slug'
  
    def get(self, request, *args, **kwargs):
        """
        This handles non-permalinked URLs according to preferences as set in
        NewsBlogConfig.
        """
        if not hasattr(self, 'object'):
            self.object = self.get_object()
        set_language_changer(request, self.object.get_absolute_url)
        url = self.object.get_absolute_url()
        if request.path == url:
            # Continue as normal
            return super(JobDetail, self).get(request, *args, **kwargs)
            

    def get_object(self, queryset=None):
        """
        Supports ALL of the types of permalinks that we've defined in urls.py.
        However, it does require that either the id and the slug is available
        and unique.
        """
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg, None)
        pk = self.kwargs.get(self.pk_url_kwarg, None)

        if pk is not None:
            # Let the DetailView itself handle this one
            return DetailView.get_object(self, queryset=queryset)
        elif slug is not None:
            # Let the TranslatedSlugMixin take over
            return super(JobDetail, self).get_object(queryset=queryset)

        raise AttributeError('JobDetail view must be called with either '
                             'an object pk or a slug')

    def get_context_data(self, **kwargs):
        context = super(JobDetail, self).get_context_data(**kwargs)
        context['prev_job'] = self.get_prev_object(
            self.queryset, self.object)
        context['next_job'] = self.get_next_object(
            self.queryset, self.object)
        return context

    def get_prev_object(self, queryset=None, object=None):
        if queryset is None:
            queryset = self.get_queryset()
        if object is None:
            object = self.get_object(self)
        prev_objs = queryset.filter(
            publishing_date__lt=object.publishing_date
        ).order_by(
            '-publishing_date'
        )[:1]
        if prev_objs:
            return prev_objs[0]
        else:
            return None

    def get_next_object(self, queryset=None, object=None):
        if queryset is None:
            queryset = self.get_queryset()
        if object is None:
            object = self.get_object(self)
        next_objs = queryset.filter(
            publishing_date__gt=object.publishing_date
        ).order_by(
            'publishing_date'
        )[:1]
        if next_objs:
            return next_objs[0]
        else:
            return None


class JobListBase(AppConfigMixin, AppHookCheckMixin,
                      PreviewModeMixin, ViewUrlMixin, ListView):
    model = Job
    show_header = False

    def get_paginate_by(self, queryset):
        if self.paginate_by is not None:
            return self.paginate_by
        else:
            try:
                return self.config.paginate_by
            except AttributeError:
                return 10  # sensible failsafe

    def get_pagination_options(self):
        # Django does not handle negative numbers well
        # when using variables.
        # So we perform the conversion here.
        if self.config:
            options = {
                'pages_start': self.config.pagination_pages_start,
                'pages_visible': self.config.pagination_pages_visible,
            }
        else:
            options = {
                'pages_start': 10,
                'pages_visible': 4,
            }

        pages_visible_negative = -options['pages_visible']
        options['pages_visible_negative'] = pages_visible_negative
        options['pages_visible_total'] = options['pages_visible'] + 1
        options['pages_visible_total_negative'] = pages_visible_negative - 1
        return options

    def get_context_data(self, **kwargs):
        context = super(JobListBase, self).get_context_data(**kwargs)
        context['pagination'] = self.get_pagination_options()
        return context


class JobList(JobListBase):
    """A complete list of jobs."""
    show_header = True

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(JobListBase, self).get_queryset()
        # prepare language properties for filtering
        return qs.translated(*self.valid_languages)


class ApplyJobFormView(AppConfigMixin, AppHookCheckMixin, PreviewModeMixin,
                    TranslatableSlugMixin,FormView):
    form_class = ApplyJobForm
    model = Applier
    template_name = 'nnuh_jobs/includes/applier_form.html'

    def get_initial(self):
        """
        We wish to record where the visitor was BEFORE arriving at the contact
        page. We'll ultimately record this in the 'referer' field in our
        model. But for now, we'll initialize our form object to include this
        here, but only when creating the original form object. This way, no
        matter how many times the visitor has validation errors, etc., we'll
        still preserve this original HTTP_REFERER.
        """
        initial = super(ApplyJobFormView, self).get_initial()
        initial['referer'] = self.request.META.get('HTTP_REFERER', ''),
        return initial
        
    def get_success_url(self):
        page = get_object_or_404(
            Page,
            reverse_id='job_form_submission',
            publisher_is_draft=False
        )
        return page.get_absolute_url()

    def form_valid(self, form):
        self.object = form.save()
        return super(ApplyJobFormView, self).form_valid(form)
