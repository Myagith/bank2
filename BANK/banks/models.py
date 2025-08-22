from django.db import models


class Bank(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
