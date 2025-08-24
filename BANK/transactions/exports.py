import csv
from io import BytesIO
from urllib.parse import urlencode
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.utils.timezone import localtime

from .models import Transaction


def _apply_filters(request, qs):
    # Applique les filtres simples présents dans l'interface
    params = request.GET
    if params.get('type'):
        qs = qs.filter(type=params['type'])
    if params.get('created_at__date__gte'):
        qs = qs.filter(created_at__date__gte=params['created_at__date__gte'])
    if params.get('created_at__date__lte'):
        qs = qs.filter(created_at__date__lte=params['created_at__date__lte'])
    if params.get('amount__gte'):
        qs = qs.filter(amount__gte=params['amount__gte'])
    if params.get('amount__lte'):
        qs = qs.filter(amount__lte=params['amount__lte'])
    return qs


def export_transactions_csv(request):
    qs = _apply_filters(request, Transaction.objects.select_related('account','account__customer'))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    w = csv.writer(response)
    w.writerow(['Date', 'Type', 'Montant', 'Compte', 'Client', 'Référence'])
    for t in qs.order_by('-created_at'):
        w.writerow([localtime(t.created_at).strftime('%Y-%m-%d %H:%M'), t.type, float(t.amount), t.account.number, str(t.account.customer), t.reference])
    return response


def export_transactions_xlsx(request):
    qs = _apply_filters(request, Transaction.objects.select_related('account','account__customer'))
    wb = Workbook()
    ws = wb.active
    ws.title = 'Transactions'
    ws.append(['Date', 'Type', 'Montant', 'Compte', 'Client', 'Référence'])
    for t in qs.order_by('-created_at'):
        ws.append([localtime(t.created_at).strftime('%Y-%m-%d %H:%M'), t.type, float(t.amount), t.account.number, str(t.account.customer), t.reference])
    bio = BytesIO()
    wb.save(bio)
    bio.seek(0)
    resp = HttpResponse(bio.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    resp['Content-Disposition'] = 'attachment; filename="transactions.xlsx"'
    return resp


def export_transactions_pdf(request):
    qs = _apply_filters(request, Transaction.objects.select_related('account','account__customer'))
    bio = BytesIO()
    c = canvas.Canvas(bio, pagesize=A4)
    width, height = A4
    y = height - 40
    c.setFont('Helvetica-Bold', 12)
    c.drawString(40, y, 'Transactions')
    y -= 20
    c.setFont('Helvetica', 10)
    c.drawString(40, y, 'Date')
    c.drawString(140, y, 'Type')
    c.drawString(220, y, 'Montant')
    c.drawString(300, y, 'Compte')
    c.drawString(420, y, 'Client')
    y -= 14
    for t in qs.order_by('-created_at')[:1000]:
        if y < 40:
            c.showPage()
            y = height - 40
        c.drawString(40, y, localtime(t.created_at).strftime('%Y-%m-%d %H:%M'))
        c.drawString(140, y, t.type[:10])
        c.drawRightString(280, y, f"{float(t.amount):.2f}")
        c.drawString(300, y, t.account.number[:14])
        c.drawString(420, y, str(t.account.customer)[:28])
        y -= 14
    c.showPage()
    c.save()
    bio.seek(0)
    resp = HttpResponse(bio.read(), content_type='application/pdf')
    resp['Content-Disposition'] = 'attachment; filename="transactions.pdf"'
    return resp

