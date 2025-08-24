from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import User
from banks.models import Bank
from customers.models import Customer
from accounts.models import Account
from transactions.models import Transaction

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
    total_banks = Bank.objects.count()
    total_customers = Customer.objects.count()
    total_accounts = Account.objects.count()
    open_accounts = Account.objects.filter(status='OPEN').count()
    closed_accounts = Account.objects.filter(status='CLOSED').count()
    by_type = (
        Account.objects.values('type').order_by('type').annotate(count=models.Count('id'))
        if hasattr(Account, 'objects') else []
    )
    recent_transactions = Transaction.objects.select_related('account','account__customer')[:10]
    context = {
        'total_banks': total_banks,
        'total_customers': total_customers,
        'total_accounts': total_accounts,
        'open_accounts': open_accounts,
        'closed_accounts': closed_accounts,
        'by_type': list(by_type),
        'recent_transactions': recent_transactions,
    }
    return render(request, 'dashboard/admin.html', context)


@login_required
def dashboard_client(request):
    # Données simples pour la démo
    return render(request, 'dashboard/client.html', {
        'total_balance': 0,
    })
