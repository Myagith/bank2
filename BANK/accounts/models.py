from django.db import models
from customers.models import Customer


class Account(models.Model):
    class AccountType(models.TextChoices):
        CHECKING = 'CHECKING', 'Checking'
        SAVINGS = 'SAVINGS', 'Savings'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        CLOSED = 'CLOSED', 'Closed'

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='accounts')
    number = models.CharField(max_length=24, unique=True)
    type = models.CharField(max_length=16, choices=AccountType.choices)
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.OPEN)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-opened_at']

    def __str__(self) -> str:
        return f"{self.number} ({self.customer})"
