from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class RequireAuthenticationMiddleware(MiddlewareMixin):
    """Redirects unauthenticated users to login page globally.

    This replaces the need for @login_required on views. It allows access to
    authentication routes, admin, and static assets without redirection.
    """

    AUTH_WHITELIST_PREFIXES = (
        '/users/login',
        '/users/logout',
        '/users/otp',
        '/admin',
        '/static',
        '/media',
    )

    def process_request(self, request):
        path = request.path
        if any(path.startswith(prefix) for prefix in self.AUTH_WHITELIST_PREFIXES):
            return None
        if not request.user.is_authenticated:
            return redirect(reverse('users:login'))
        # Enforce OTP 2FA: require session flag after login
        if not request.session.get('otp_ok') and not path.startswith('/users/otp'):
            return redirect(reverse('users:otp_verify'))
        return None