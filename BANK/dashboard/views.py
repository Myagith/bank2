from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime, timedelta
from customers.models import Customer
from accounts.models import Account
from transactions.models import Transaction

# Create your views here.


def index(request):
    return render(request, 'dashboard/index.html')


def client(request):
    # Try to resolve a customer for the logged-in user by email
    customer = None
    if request.user and request.user.is_authenticated:
        customer = Customer.objects.filter(email=request.user.email).first()

    accounts = Account.objects.filter(customer=customer) if customer else Account.objects.none()
    accounts_count = accounts.count()

    main_account = accounts.order_by('-opened_at').first()
    main_account_balance = main_account.balance if main_account else 0

    tx_qs = Transaction.objects.filter(account__in=accounts)

    total_deposits = (
        tx_qs.filter(type=Transaction.Type.DEPOSIT).aggregate(s=Sum('amount')).get('s') or 0
    )
    total_expenses = (
        tx_qs.exclude(type=Transaction.Type.DEPOSIT).aggregate(s=Sum('amount')).get('s') or 0
    )

    recent_transactions = list(tx_qs.select_related('account').order_by('-created_at')[:10])

    # Prepare last 7 days expenses
    days = 7
    today = datetime.utcnow().date()
    labels = []
    values = []
    for i in range(days-1, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime('%d/%m'))
        day_total = tx_qs.exclude(type=Transaction.Type.DEPOSIT).filter(
            created_at__date=day
        ).aggregate(s=Sum('amount')).get('s') or 0
        values.append(float(day_total))

    client_dashboard_data = {
        'total_deposits': float(total_deposits),
        'total_expenses': float(total_expenses),
        'last_days_labels': labels,
        'last_days_expenses': values,
    }

    context = {
        'main_account_balance': main_account_balance,
        'accounts_count': accounts_count,
        'recent_transactions': recent_transactions,
        'client_dashboard_data': client_dashboard_data,
    }
    return render(request, 'dashboard/client.html', context)
