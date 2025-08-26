from django.urls import path
from . import views, api

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('client/', views.client, name='client'),
    path('api/transactions/monthly/', api.transactions_monthly, name='transactions_monthly'),
    path('api/banks/top15/', api.banks_top15, name='banks_top15'),
]