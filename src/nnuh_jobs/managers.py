# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db.models import Q

from django.utils.timezone import now

from aldryn_apphooks_config.managers.base import ManagerMixin, QuerySetMixin
from parler.managers import TranslatableManager, TranslatableQuerySet



class JobQuerySet(QuerySetMixin, TranslatableQuerySet):
    # def published(self):
    #     """
    #     Returns jobs that are published AND have a publishing_date that
    #     has actually passed.
    #     """
    #     return self.filter(is_published=True, publishing_date__lte=now())
    
    def active(self):
        return self.filter(
            Q(publishing_date__isnull=True) | Q(publishing_date__lte=now()),
            Q(deadline_date__isnull=True) | Q(deadline_date__gt=now()),
            is_active=True
        )



class RelatedManager(ManagerMixin, TranslatableManager):
    def get_queryset(self):
        qs = JobQuerySet(self.model, using=self.db)
        return qs.select_related('featured_image')

    def published(self):
        return self.get_queryset().published()