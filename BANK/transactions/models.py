from django.db import models
from accounts.models import Account


class Transaction(models.Model):
    class Type(models.TextChoices):
        TRANSFER = 'TRANSFER', 'Transfer'
        DEPOSIT = 'DEPOSIT', 'Deposit'
        WITHDRAW = 'WITHDRAW', 'Withdraw'

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=16, choices=Type.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.type} {self.amount} on {self.account}"
