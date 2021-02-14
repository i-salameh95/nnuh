from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

from nnuh_search.cms_menus import GenerateReverseIdModifier


class NnuhSearchApphook(CMSApp):
    name = _("NNUH Search")
    app_name = 'nnuh_search'



    def get_urls(self, *args, **kwargs):
        return ['nnuh_search.urls']

    def get_menus(self, page=None, language=None, **kwargs):
        return [GenerateReverseIdModifier]


apphook_pool.register(NnuhSearchApphook)
