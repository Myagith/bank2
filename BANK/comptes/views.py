from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth

from banks.models import Bank
from customers.models import Customer
from accounts.models import Account
from transactions.models import Transaction

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
    # Global KPIs
    banks_count = Bank.objects.count()
    customers_count = Customer.objects.count()
    accounts_open_count = Account.objects.filter(status=Account.Status.OPEN).count()

    # Top 15 banks by number of customers
    top_banks = (
        Bank.objects
        .annotate(num_customers=Count('customers'))
        .order_by('-num_customers')[:15]
        .values('name', 'country', 'city', 'num_customers')
    )

    # Charts
    clients_by_bank = list(
        Bank.objects.annotate(num_customers=Count('customers')).order_by('-num_customers').values('name', 'num_customers')
    )

    tx_monthly = (
        Transaction.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    tx_chart = {
        'labels': [x['month'].strftime('%b %Y') if x['month'] else '' for x in tx_monthly],
        'values': [float(x['total'] or 0) for x in tx_monthly],
    }

    # Scoped stats for admin's own bank (if any)
    scoped = {}
    if getattr(request.user, 'bank_id', None):
        b_id = request.user.bank_id
        scoped['clients_total'] = Customer.objects.filter(bank_id=b_id).count()
        scoped['accounts_total'] = Account.objects.filter(customer__bank_id=b_id).count()
        scoped['accounts_closed'] = Account.objects.filter(customer__bank_id=b_id, status=Account.Status.CLOSED).count()
        scoped['accounts_closing'] = Account.objects.filter(customer__bank_id=b_id, status=Account.Status.CLOSING).count()
        type_breakdown = (
            Account.objects.filter(customer__bank_id=b_id)
            .values('type').annotate(c=Count('id')).order_by('-c')
        )
        scoped['types'] = list(type_breakdown)
        recent_txs = (
            Transaction.objects.filter(account__customer__bank_id=b_id)
            .select_related('account')[:10]
        )
    else:
        recent_txs = Transaction.objects.select_related('account')[:10]

    context = {
        'banks_count': banks_count,
        'customers_count': customers_count,
        'accounts_open_count': accounts_open_count,
        'top_banks': list(top_banks),
        'clients_by_bank': clients_by_bank,
        'tx_chart': tx_chart,
        'scoped': scoped,
        'recent_txs': recent_txs,
    }
    return render(request, 'comptes/dashboard_admin.html', context)


@login_required
@role_required('CLIENT', 'ADMIN')
def dashboard_client(request):
    # If admin visits client dashboard, show empty client context
    customer = getattr(request.user, 'customer', None)

    accounts = Account.objects.none()
    cards = []  # Placeholder if a Card model existed
    transactions = Transaction.objects.none()
    totals = {'accounts_open': 0, 'balance_total': 0}

    if customer:
        accounts = customer.accounts.all().select_related('customer')
        transactions = Transaction.objects.filter(account__customer=customer)[:20]
        totals['accounts_open'] = accounts.filter(status=Account.Status.OPEN).count()
        totals['balance_total'] = float(accounts.aggregate(s=Sum('balance'))['s'] or 0)

    # Monthly deposits vs withdrawals chart
    monthly = (
        Transaction.objects.filter(account__customer=customer) if customer else Transaction.objects.none()
    )
    monthly = (
        monthly.annotate(month=TruncMonth('created_at'))
        .values('month', 'type')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    months = sorted({x['month'].strftime('%b %Y') for x in monthly if x['month']})
    deposits = {m: 0 for m in months}
    withdraws = {m: 0 for m in months}
    for x in monthly:
        if not x['month']:
            continue
        m = x['month'].strftime('%b %Y')
        amt = float(x['total'] or 0)
        if x['type'] == Transaction.Type.DEPOSIT:
            deposits[m] = amt
        elif x['type'] in (Transaction.Type.WITHDRAW, Transaction.Type.TRANSFER):
            withdraws[m] = amt

    context = {
        'customer': customer,
        'accounts': accounts,
        'cards': cards,
        'transactions': transactions,
        'totals': totals,
        'chart_labels': months,
        'chart_deposits': [deposits[m] for m in months],
        'chart_withdraws': [withdraws[m] for m in months],
    }
    return render(request, 'comptes/dashboard_client.html', context)


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