# from distutils.command.clean import clean
# from django import forms
# from django.utils.translation import ugettext_lazy as _

# from nnuh_jobs.models import Applier,Job, JobApplication
# from django.shortcuts import get_object_or_404
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Submit,Fieldset,ButtonHolder,Row
# from django.core.validators import EMPTY_VALUES

# class ApplyJobForm(forms.ModelForm):

#     class Meta:
#         model = Applier
#         fields = '__all__'
#         widgets = {
#             'relations': forms.RadioSelect
#         }
#     def __init__(self, *args, **kwargs):
#         job_id = kwargs.pop('job_id')
#         job = get_object_or_404(Job,pk=job_id)
#         super(ApplyJobForm, self).__init__(*args, **kwargs) 
#         self.helper = FormHelper()
#         self.helper.form_tag = False
#         self.helper.disable_csrf = True
#         self.helper.include_media = False
#         self.helper.form_class = 'form-horizontal'
#         self.helper.layout = Layout(
#             Fieldset(_('Basic Information'),
#                 'first_name',
#                 'second_name',
#                 'third_name',
#                 'family',
#                 'sex',
#                 'card_id_number',
#                 'date_of_birth',
#             ),
#             Fieldset(_('Contact details'),
#                 'tel_no',
#                 'mob_no',
#                 Row('email1', 'verify_email',css_class='form-row'),
#                 'address',
#             ),
#             Fieldset(_('Relations'),
#                 'relations',
#                 'relative_name',
#                 'relation_type',
#             ),
            
#         )
#         if not job.cv_option:
#             self.fields.pop('cv')
#         if not job.tawjihi_option:
#             self.fields.pop('tawjihi')
#         if not job.certificate_option:
#             self.fields.pop('certificate')
#         if not job.ID_option:
#             self.fields.pop('card_ID_file')
#         if not job.personal_photo_option:
#             self.fields.pop('personal_photo')
#         if not job.work_cert_option:
#             self.fields.pop('work_cert')
#         if not job.org_cert_option:
#             self.fields.pop('org_cert')
#         if not job.recommendation_letters_option:
#             self.fields.pop('recommendation_letters')
#         if not job.personal_statment_option:
#             self.fields.pop('personal_statment')
#         if not job.marks_list_option:
#             self.fields.pop('marks_list')
#         if not job.insurance_doc_option:
#             self.fields.pop('insurance_doc')

#         self.helper.render_unmentioned_fields = True

#     def clean_email1(self):
#         email1 = self.cleaned_data.get("email1")
#         email2 = self.cleaned_data.get("verify_email")
#         if email1 and email2 and email2  != email1:
#             self.add_error('verify_email', _("Emails doesnt match each other"))
#         return self.cleaned_data

#     def clean_relations(self):
#         have_relations =  self.cleaned_data.get('relations')
#         if have_relations:
#             relative_name = self.cleaned_data.get('relative_name')
#             relation_type = self.cleaned_data.get('relation_type')
#             if relative_name or relation_type in EMPTY_VALUES:
#                 self.add_error('relative_name',_("relative name must be filled"))
#         return self.cleaned_data
