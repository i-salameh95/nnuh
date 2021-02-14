from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ContactMessage(models.Model):
    name = models.CharField(
        verbose_name=_('Full Name'), max_length=255)
    phone = models.CharField(
        verbose_name=_('Phone/Mobile'), max_length=255)
    email = models.CharField(
        verbose_name=_('Email Address'), max_length=255, blank=True)
    # birth_date = models.CharField(
    #     verbose_name=_('Birth Date'), max_length=255, blank=True)
    message = models.TextField(
        verbose_name=_('Message'), blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')
        ordering = ['-created_at']

    def __str__(self):
        return '{}'.format(self.name)




class ContactFormPluginModel(CMSPlugin):
    def __str__(self):
        if self.recipients.exists():
            return self.recipients.first().email
        return 'ContactFormPlugin'

    def copy_relations(self, oldinstance):
        self.recipients.all().delete()
        for recipient in oldinstance.recipients.all():
            recipient.pk = None
            recipient.plugin = self
            recipient.save()


class Recipient(models.Model):
    plugin = models.ForeignKey(ContactFormPluginModel, verbose_name=_('Plugin'), related_name='recipients', on_delete=models.CASCADE)
    email = models.EmailField(verbose_name=_('Recipient Email'))

    def __str__(self):
        return self.email
