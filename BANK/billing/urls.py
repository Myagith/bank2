from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('create/', views.InvoiceCreateView.as_view(), name='create'),
    path('<int:pk>/send/', views.invoice_send, name='send'),
]