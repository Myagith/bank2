from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse

from .forms import RegisterForm, LoginForm, OTPVerifyForm
from .models import User
from .services import send_otp_email, send_welcome_email


def _render(request, template, context=None):
    return render(request, template, context or {})


@user_passes_test(lambda u: u.is_authenticated and getattr(u, 'is_admin', False))
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            raw_password = form.cleaned_data['password']
            user: User = form.save(commit=False)
            user.set_password(raw_password)
            # Admin creates the user; enable login and mark email verified by default
            user.can_login = True
            user.save()
            try:
                send_welcome_email(user, raw_password)
            except Exception:
                pass
            messages.success(request, 'Utilisateur créé et email de bienvenue envoyé.')
            return redirect('dashboard:index')
    else:
        form = RegisterForm()
    return _render(request, 'users/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            auth_login(request, user)
            request.session['otp_ok'] = False
            send_otp_email(user)
            messages.info(request, 'Check your email for the 6-digit code.')
            return redirect('users:otp_verify')
    else:
        form = LoginForm()
    return _render(request, 'users/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.success(request, 'Logged out.')
    return redirect('users:login')


def otp_verify(request):
    if request.method == 'POST':
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['otp_code']
            user: User = request.user
            if not user or not user.otp_code:
                messages.error(request, 'No OTP pending.')
                return redirect('users:login')
            if timezone.now() > (user.otp_expires_at or timezone.now()):
                messages.error(request, 'Code expired. New code sent.')
                send_otp_email(user)
                return redirect('users:otp_verify')
            if code != user.otp_code:
                messages.error(request, 'Invalid code.')
                return redirect('users:otp_verify')
            # success -> redirect by role
            request.session['otp_ok'] = True
            user.otp_code = None
            user.otp_expires_at = None
            user.save(update_fields=['otp_code', 'otp_expires_at'])
            if user.role == User.Role.ADMIN:
                return redirect('dashboard:admin')
            return redirect('dashboard:client')
    else:
        form = OTPVerifyForm()
    return _render(request, 'users/otp_verify.html', {'form': form})
