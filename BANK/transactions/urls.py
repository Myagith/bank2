from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('create/', views.TransactionCreateView.as_view(), name='create'),
    path('history/', views.TransactionHistoryView.as_view(), name='history'),
]