from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'transaction', 'amount', 'status', 'issued_at')
    list_filter = ('status',)
    search_fields = ('id', 'account__number')
