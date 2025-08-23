from django.db import models
from accounts.models import Account
from transactions.models import Transaction


class Invoice(models.Model):
    class Status(models.TextChoices):
        SENT = 'SENT', 'Envoyée'
        PENDING = 'PENDING', 'En attente'

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='invoices')
    transaction = models.ForeignKey(Transaction, null=True, blank=True, on_delete=models.SET_NULL, related_name='invoices')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='invoices/')
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)

    class Meta:
        ordering = ['-issued_at']

    def __str__(self) -> str:
        return f"Invoice {self.pk} - {self.amount}"
