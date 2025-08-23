from django.db import models
from datetime import date


class Bank(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.CharField(max_length=255, blank=True)  # propriétaire
    country = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=32)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def age(self) -> int:
        # years between today and created_at.date()
        if not self.created_at:
            return 0
        today = date.today()
        started = self.created_at.date()
        return today.year - started.year - ((today.month, today.day) < (started.month, started.day))
