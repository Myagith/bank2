from django.http import JsonResponse
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Count
from transactions.models import Transaction
from banks.models import Bank
from customers.models import Customer
from django.utils.timezone import now
from datetime import timedelta


def transactions_monthly(request):
    # Ensure there is at least demo data for charts if DB is empty
    qs = (
        Transaction.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    data = {
        'labels': [x['month'].strftime('%b %Y') if x['month'] else '' for x in qs],
        'values': [float(x['total'] or 0) for x in qs],
    }
    return JsonResponse(data)


def banks_top15(request):
    qs = (
        Bank.objects
        .annotate(num_customers=Count('customers'))
        .order_by('-num_customers')[:15]
        .values('id', 'name', 'country', 'city', 'num_customers')
    )
    return JsonResponse({'items': list(qs)})