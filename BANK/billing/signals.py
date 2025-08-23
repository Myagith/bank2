from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from banks.models import Bank
from customers.models import Customer
from .models import Invoice


@receiver(post_save, sender=Bank)
def bank_welcome_email(sender, instance: Bank, created: bool, **kwargs):
    if not created:
        return
    subject = f"Bienvenue {instance.name}"
    body = render_to_string('emails/bank_welcome.txt', {'bank': instance})
    EmailMessage(subject, body, to=[instance.email]).send(fail_silently=True)


@receiver(post_save, sender=Customer)
def customer_welcome_email(sender, instance: Customer, created: bool, **kwargs):
    if not created:
        return
    subject = "Bienvenue"
    body = render_to_string('emails/customer_welcome.txt', {'customer': instance})
    EmailMessage(subject, body, to=[instance.email]).send(fail_silently=True)


@receiver(post_save, sender=Invoice)
def invoice_send_email(sender, instance: Invoice, created: bool, **kwargs):
    if not created:
        return
    subject = f"Facture #{instance.pk}"
    body = render_to_string('emails/invoice_created.txt', {'invoice': instance})
    email = EmailMessage(subject, body, to=[instance.account.customer.email])
    if instance.pdf_file:
        email.attach_file(instance.pdf_file.path)
    email.send(fail_silently=True)