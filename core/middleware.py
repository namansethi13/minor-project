from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.utils.functional import SimpleLazyObject
from django.contrib.admin import AdminSite

class DisableCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        admin_site = SimpleLazyObject(lambda: AdminSite())
        resolver_match = getattr(request, 'resolver_match', None)
        if resolver_match is not None and (request.path.startswith(reverse('admin:index')) or admin_site.is_registered(resolver_match.func.cls)):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None
