import csv
from io import BytesIO, StringIO
from django.http import HttpResponse
from django.db.models import Count
from openpyxl import Workbook
from banks.models import Bank


def _top15_queryset(request):
    qs = Bank.objects.annotate(num_customers=Count('customers')).order_by('-num_customers')[:15]
    return qs


def top_banks_csv(request):
    qs = _top15_queryset(request)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="top_banks.csv"'
    writer = csv.writer(response)
    writer.writerow(['Rang','Banque','Clients','Pays','Ville'])
    for i, b in enumerate(qs, start=1):
        writer.writerow([i, b.name, getattr(b, 'num_customers', 0), b.country, b.city])
    return response


def top_banks_xlsx(request):
    qs = _top15_queryset(request)
    wb = Workbook()
    ws = wb.active
    ws.append(['Rang','Banque','Clients','Pays','Ville'])
    for i, b in enumerate(qs, start=1):
        ws.append([i, b.name, getattr(b, 'num_customers', 0), b.country, b.city])
    bio = BytesIO()
    wb.save(bio)
    bio.seek(0)
    response = HttpResponse(bio.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="top_banks.xlsx"'
    return response
