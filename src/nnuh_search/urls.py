from django.conf.urls import url

from nnuh_search.views import NnuhSearchView


urlpatterns = [
    url('^$', NnuhSearchView.as_view(), name='nnuh-search'),
]