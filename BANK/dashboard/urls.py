from django.urls import path
from . import views, api
from . import exports

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', views.dashboard_admin, name='admin'),
    path('client/', views.dashboard_client, name='client'),
    path('api/transactions/monthly/', api.transactions_monthly, name='transactions_monthly'),
    path('api/transactions/monthly-by-type/', api.transactions_monthly_by_type, name='transactions_monthly_by_type'),
    path('api/banks/top15/', api.banks_top15, name='banks_top15'),
    path('export/top-banks.csv', exports.top_banks_csv, name='export_top_banks_csv'),
    path('export/top-banks.xlsx', exports.top_banks_xlsx, name='export_top_banks_xlsx'),
]