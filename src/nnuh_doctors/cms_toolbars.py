# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import get_language_from_request, ugettext as _

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse

from parler.models import TranslatableModel
from six import iteritems

from .models import Section, Doctor


def get_obj_from_request(model, request,
                         pk_url_kwarg='pk',
                         slug_url_kwarg='slug',
                         slug_field='slug'):
    """
    Given a model and the request, try to extract and return an object
    from an available 'pk' or 'slug', or return None.

    Note that no checking is done that the view's kwargs really are for objects
    matching the provided model (how would it?) so use only where appropriate.
    """
    language = get_language_from_request(request, check_path=True)
    kwargs = request.resolver_match.kwargs
    mgr = model.objects
    if pk_url_kwarg in kwargs:
        return mgr.filter(pk=kwargs[pk_url_kwarg]).first()
    elif slug_url_kwarg in kwargs:
        # If the model is translatable, and the given slug is a translated
        # field, then find it the Parler way.
        filter_kwargs = {slug_field: kwargs[slug_url_kwarg]}
        translated_fields = model._parler_meta.get_translated_fields()
        if issubclass(model, TranslatableModel) and slug_url_kwarg in translated_fields:
            return mgr.active_translations(language, **filter_kwargs).first()
        else:
            # OK, do it the normal way.
            return mgr.filter(**filter_kwargs).first()
    else:
        return None


def get_admin_url(action, action_args=[], **url_args):
    """
    Convenience method for constructing admin-urls with GET parameters.
    """
    base_url = admin_reverse(action, args=action_args)
    # Converts [{key: value}, …] => ["key=value", …]
    url_arg_list = sorted(iteritems(url_args))
    params = ["=".join([str(k), str(v)]) for (k, v) in url_arg_list]
    if params:
        return "?".join([base_url, "&".join(params)])
    else:
        return base_url


@toolbar_pool.register
class PeopleToolbar(CMSToolbar):
    # watch_models must be a list, not a tuple
    # see https://github.com/divio/django-cms/issues/4135
    watch_models = [Doctor, Section, ]
    supported_apps = ('nnuh_doctors', )

    def populate(self):
        user = getattr(self.request, 'user', None)
        try:
            view_name = self.request.resolver_match.view_name
        except AttributeError:
            view_name = None

        if user and view_name:
            language = get_language_from_request(self.request, check_path=True)
            section = doctor = None
            if view_name == 'nnuh_doctors:section-detail':
                section = get_obj_from_request(Section, self.request)
            elif view_name in [
                    'nnuh_doctors:doctor-detail',
                    'nnuh_doctors:download_vcard']:
                doctor = get_obj_from_request(Doctor, self.request)
                if doctor:
                    section = doctor.section
            elif view_name in ['nnuh_doctors:doctor-list', ]:
                pass
            else:
                # We don't appear to be on any nnuh_doctors views so this
                # menu shouldn't even be here.
                return

            menu = self.toolbar.get_or_create_menu('doctors-app', "Doctors")
            change_section_perm = user.has_perm('nnuh_doctors.change_section')
            add_section_perm = user.has_perm('nnuh_doctors.add_section')
            section_perms = [change_section_perm, add_section_perm]

            change_doctor_perm = user.has_perm('nnuh_doctors.change_doctor')
            add_doctor_perm = user.has_perm('nnuh_doctors.add_doctor')
            doctor_perms = [change_doctor_perm, add_doctor_perm]

            if change_section_perm:
                url = admin_reverse('nnuh_doctors_section_changelist')
                menu.add_sideframe_item(_('Section list'), url=url)

            if add_section_perm:
                url_args = {}
                if language:
                    url_args.update({"language": language})
                url = get_admin_url('nnuh_doctors_section_add', **url_args)
                menu.add_modal_item(_('Add new section'), url=url)

            if change_section_perm and section:
                url = get_admin_url('nnuh_doctors_section_change', [section.pk, ])
                menu.add_modal_item(_('Edit section'), url=url, active=True)

            if any(section_perms) and any(doctor_perms):
                menu.add_break()

            if change_doctor_perm:
                url = admin_reverse('nnuh_doctors_doctor_changelist')
                menu.add_sideframe_item(_('Doctor list'), url=url)

            if add_doctor_perm:
                url_args = {}
                if section:
                    url_args['sections'] = section.pk
                if language:
                    url_args['language'] = language
                url = get_admin_url('nnuh_doctors_doctor_add', **url_args)
                menu.add_modal_item(_('Add new doctor'), url=url)

            if change_doctor_perm and doctor:
                url = admin_reverse(
                    'nnuh_doctors_doctor_change', args=(doctor.pk, ))
                menu.add_modal_item(_('Edit doctor'), url=url, active=True)
