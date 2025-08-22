from django.db import models
from banks.models import Bank


class Customer(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    client_no = models.CharField(max_length=32, unique=True)
    phone = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["email"]),
            models.Index(fields=["client_no"]),
        ]
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.client_no})"
