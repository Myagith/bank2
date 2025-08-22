from django.urls import path
from . import views

app_name = 'banks'

urlpatterns = [
    path('', views.BankListView.as_view(), name='list'),
    path('create/', views.BankCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.BankUpdateView.as_view(), name='update'),
    path('<int:pk>/', views.BankDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.BankDeleteView.as_view(), name='delete'),
    path('top-15/', views.BankTop15View.as_view(), name='top15'),
]