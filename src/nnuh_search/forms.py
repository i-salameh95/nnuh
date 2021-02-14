from aldryn_newsblog.models import Article
from crispy_forms.bootstrap import InlineField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML
from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext

from haystack.forms import SearchForm

from nnuh_doctors.models import Doctor


class NnuhSearchForm(SearchForm):
    model_type = forms.ChoiceField(
        label=_('Search Type'), choices=(
                ('', _('Search for all Data')),
                ('doctors', _('Doctors')),
                ('news', _('News & Announcements')),
            ), required=False, initial=None )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].label = _('Search for')
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.include_media = False
        self.helper.layout = Layout(
            Div(
                HTML('<h3 class="d-none d-lg-block w-25 my-3 display-4 text-white">{}:</h3>'.format(_('Search'))),
                Div(
                    Div(InlineField('q'), css_class='col-10 col-md-5'),
                    Div(InlineField('model_type'), css_class='col-10 col-md-5'),
                    Div(HTML('<button type="submit" class="btn btn-violet">'
                             '<i class="fas fa-search"></i>'
                             '</button>'),
                        css_class='col-2 col-md-2'),
                    css_class='row flex-grow-1'
                ),
                css_class='d-flex justify-content-between align-items-center'
            )
        )

    def search(self):
        sqs = super(NnuhSearchForm, self).search()

        if self.cleaned_data['model_type'] == 'doctors':
            print("*"*80, 'doctors')
            sqs = sqs.models(Doctor)
        elif self.cleaned_data['model_type'] == 'news':
            print("*"*80, 'news')
            sqs = sqs.models(Article)

        return sqs
