from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("client_no", "name", "email", "bank")
    search_fields = ("client_no", "name", "email")
    list_filter = ("bank",)
