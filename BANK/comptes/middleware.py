from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    ALLOWED_PREFIXES = (
        '/comptes/login',
        '/comptes/logout',
        '/admin',
        '/static',
        '/media',
    )

    def process_request(self, request):
        path = request.path
        if any(path.startswith(prefix) for prefix in self.ALLOWED_PREFIXES):
            return None
        if not request.user.is_authenticated:
            return redirect(reverse('comptes:login'))
        return None