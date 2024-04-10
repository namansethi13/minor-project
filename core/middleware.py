from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest

class DisableCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Ensure the request is an instance of HttpRequest
        if not isinstance(request, HttpRequest):
            return None
        
        # Check if the request path starts with the desired admin URL
        if request.path.startswith('/accounts/api_admin/') or request.path.startswith('/results/api_admin/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None
