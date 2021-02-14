from nnuh_search.forms import NnuhSearchForm


def search_form(request):
    return {
        'SEARCH_FORM': NnuhSearchForm(initial=request.GET)
    }