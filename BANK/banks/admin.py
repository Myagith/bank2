from django.contrib import admin
from .models import Bank


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "city", "email", "phone")
    search_fields = ("name", "country", "city")
