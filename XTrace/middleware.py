from django.http import HttpResponseForbidden
from django.shortcuts import redirect

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if request.user.is_authenticated:
                # Only superusers and Admin group can access Django admin
                if not request.user.is_superuser and not request.user.groups.filter(name='Admin').exists():
                    return HttpResponseForbidden('Access denied. Only Admin group can access Django admin panel.')
            
        return self.get_response(request)
