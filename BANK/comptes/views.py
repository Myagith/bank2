from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import LoginForm, UserPasswordChangeForm
from .decorators import role_required


def login_view(request):
    if request.user.is_authenticated:
        return redirect('comptes:dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            first_login = getattr(user, 'last_login', None) is None
            auth_login(request, user)
            messages.success(request, 'Connexion réussie.')
            if first_login:
                messages.info(request, 'Veuillez changer votre mot de passe.')
                return redirect('comptes:change_password')
            return redirect('comptes:dashboard')
    else:
        form = LoginForm(request)
    return render(request, 'comptes/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    messages.success(request, 'Déconnexion réussie.')
    return redirect('comptes:login')


@login_required
def dashboard(request):
    user = request.user
    if getattr(user, 'role', None) == 'ADMIN':
        return redirect('comptes:dashboard_admin')
    return redirect('comptes:dashboard_client')


@login_required
@role_required('ADMIN')
def dashboard_admin(request):
    return render(request, 'comptes/dashboard_admin.html')


@login_required
@role_required('CLIENT', 'ADMIN')
def dashboard_client(request):
    return render(request, 'comptes/dashboard_client.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mot de passe modifié avec succès.')
            return redirect('comptes:dashboard')
    else:
        form = UserPasswordChangeForm(user=request.user)
    return render(request, 'comptes/change_password.html', {'form': form})