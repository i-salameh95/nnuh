
class ForceResponseMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method == "POST" and getattr(request, 'nnuh_contact_redirect_to', None):
            return request.nnuh_contact_redirect_to
        return response
