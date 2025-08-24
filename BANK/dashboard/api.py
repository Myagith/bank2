from django.http import JsonResponse
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Count, Q
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
    created_after = request.GET.get('year_after')
    min_clients = request.GET.get('min_clients')
    qs = Bank.objects.annotate(num_customers=Count('customers'))
    if created_after and created_after.isdigit():
        qs = qs.filter(created_at__year__gt=int(created_after))
    if min_clients and min_clients.isdigit():
        qs = qs.filter(num_customers__gte=int(min_clients))
    qs = qs.order_by('-num_customers')[:15].values('id','name','country','city','num_customers')
    return JsonResponse({'items': list(qs)})


def transactions_monthly_by_type(request):
    qs = (
        Transaction.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(
            dep=Sum('amount', filter=Q(type='DEPOSIT')),
            wit=Sum('amount', filter=Q(type='WITHDRAW')),
        )
        .order_by('month')
    )
    data = {
        'labels': [x['month'].strftime('%b %Y') if x['month'] else '' for x in qs],
        'deposit': [float(x['dep'] or 0) for x in qs],
        'withdraw': [float(x['wit'] or 0) for x in qs],
    }
    return JsonResponse(data)