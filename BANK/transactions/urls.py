from django.urls import path
from . import views
from . import exports

app_name = 'transactions'

urlpatterns = [
    path('create/', views.TransactionCreateView.as_view(), name='create'),
    path('history/', views.TransactionHistoryView.as_view(), name='history'),
    path('export/csv/', exports.export_transactions_csv, name='export_csv'),
    path('export/xlsx/', exports.export_transactions_xlsx, name='export_xlsx'),
    path('export/pdf/', exports.export_transactions_pdf, name='export_pdf'),
]