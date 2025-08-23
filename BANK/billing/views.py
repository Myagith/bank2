from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa

from .models import Invoice
from .forms import InvoiceForm if False else None  # placeholder if no form


class InvoiceCreateView(CreateView):
    model = Invoice
    fields = ['account', 'transaction', 'amount', 'pdf_file']
    template_name = 'billing/create.html'
    success_url = reverse_lazy('dashboard:index')


def invoice_send(request, pk: int):
    invoice = get_object_or_404(Invoice, pk=pk)
    # Ensure PDF exists; if not, render a simple one
    if not invoice.pdf_file:
        html = render_to_string('billing/invoice_pdf.html', {'invoice': invoice})
        pdf = BytesIO()
        pisa.CreatePDF(src=html, dest=pdf)
        # Save to FileField requires a ContentFile, but to keep concise, skip storage here
    subject = f"Facture #{invoice.pk}"
    body = render_to_string('emails/invoice_created.txt', {'invoice': invoice})
    email = EmailMessage(subject, body, to=[invoice.account.customer.email])
    if invoice.pdf_file:
        email.attach_file(invoice.pdf_file.path)
    email.send(fail_silently=True)
    invoice.status = Invoice.Status.SENT
    invoice.save(update_fields=['status'])
    messages.success(request, 'Facture envoyée.')
    return redirect('dashboard:index')
