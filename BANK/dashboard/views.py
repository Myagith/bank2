from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import User
from banks.models import Bank
from customers.models import Customer
from accounts.models import Account

# Create your views here.


def index(request):
    # Redirect based on role after login/OTP
    if not request.user.is_authenticated:
        return redirect('users:login')
    if getattr(request.user, 'role', None) == User.Role.ADMIN:
        return redirect('dashboard:admin')
    return redirect('dashboard:client')


@login_required
def dashboard_admin(request):
    context = {
        'total_banks': Bank.objects.count(),
        'total_customers': Customer.objects.count(),
        'total_accounts': Account.objects.count(),
    }
    return render(request, 'dashboard/admin.html', context)


@login_required
def dashboard_client(request):
    # Données simples pour la démo
    return render(request, 'dashboard/client.html', {
        'total_balance': 0,
    })
