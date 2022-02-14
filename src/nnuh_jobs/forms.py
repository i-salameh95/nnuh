from django.utils.translation import ugettext_lazy as _
from parler.forms import TranslatableModelForm

from nnuh_jobs.models import Applier


class ApplyJobForm(TranslatableModelForm):

    class Meta:
        model = Applier
        fields = '__all__'

    def clean(self):
        cleaned_data =  super().clean()
        email1 = cleaned_data.get("email")
        email2 = cleaned_data.get("verify_email")

        if email1 and email2 and email2  != email1:
              self.add_error('verify_email', "emails does not match")
        return cleaned_data
    



