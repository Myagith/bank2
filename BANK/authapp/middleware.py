from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    ALLOWED_PREFIXES = (
        '/auth/login',
        '/auth/logout',
        '/admin',
        '/static',
        '/media',
    )

    def process_request(self, request):
        path = request.path
        if any(path.startswith(prefix) for prefix in self.ALLOWED_PREFIXES):
            return None
        if not request.user.is_authenticated:
            return redirect('authapp:login')
        return None