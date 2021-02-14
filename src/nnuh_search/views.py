from django.shortcuts import render
from haystack.generic_views import SearchView

from nnuh_search.forms import NnuhSearchForm


class NnuhSearchView(SearchView):
    form_class = NnuhSearchForm
    template_name = 'nnuh_search/search.html'
    context_object_name = 'object_list'

