# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from aldryn_people.utils import get_valid_languages
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.utils.translation import get_language_from_request
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from menus.utils import set_language_changer
from parler.views import TranslatableSlugMixin

from nnuh_doctors.forms import AppointmentForm, NnuhDoctorSectionSearchForm

from . import DEFAULT_APP_NAMESPACE
from .models import Doctor, Section


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


class DoctorDetail(LanguageChangerMixin, AllowPKsTooMixin,
                        TranslatableSlugMixin, DetailView):
    model = Doctor
    template_name = 'nnuh_doctors/doctor_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.get_object()
        context.update({
            'form': AppointmentForm(initial={'doctor': doctor})
        })
        return context


class MakeAppointment(LanguageChangerMixin, AllowPKsTooMixin, TranslatableSlugMixin, SingleObjectMixin, FormView):
    model = Doctor
    form_class = AppointmentForm
    template_name = 'nnuh_doctors/doctor_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_initial(self):
        initial = super(MakeAppointment, self).get_initial()
        initial['doctor'] = self.get_object()
        return initial

    def get_success_url(self):
        return self.getobject().get_absolute_url()

    def form_valid(self, form):
        # super(MakeAppointment, self).form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, _('Appointment has been received successfully.'))
        form.save()
        return redirect(self.get_object())

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, _('Please correct errors.'))
        return super().form_invalid(form)


class DoctorDetailView(View):

    def get(self, request, *args, **kwargs):
        view = DoctorDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = MakeAppointment.as_view()
        return view(request, *args, **kwargs)


class SectionDetailView(LanguageChangerMixin, AllowPKsTooMixin,
                        TranslatableSlugMixin, DetailView):
    model = Section


class DoctorListView(ListView):
    model = Doctor
    paginate_by = 12
    form_class = NnuhDoctorSectionSearchForm

    def dispatch(self, request, *args, **kwargs):
        self.request_language = get_language(request)
        self.request = request
        self.site_id = getattr(get_current_site(self.request), 'id', None)
        self.valid_languages = get_valid_languages(
            DEFAULT_APP_NAMESPACE, self.request_language, self.site_id)
        return super(DoctorListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(DoctorListView, self).get_queryset()
        # prepare language properties for filtering
        doctor_type = self.request.GET.get('doctor_type')
        section_type = self.request.GET.get('section_type')
        
        doctor_list = Doctor.objects.all()
        if doctor_type:
            qs = doctor_list.filter(pk = doctor_type)
        if section_type:
            qs = doctor_list.filter(section_id= section_type)
        if doctor_type and section_type:
            qs = doctor_list
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NnuhDoctorSectionSearchForm(self.request.GET)
        return context
