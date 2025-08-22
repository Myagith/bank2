from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.AccountListView.as_view(), name='list'),
    path('create/', views.AccountCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.AccountUpdateView.as_view(), name='update'),
    path('<int:pk>/', views.AccountDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.AccountDeleteView.as_view(), name='delete'),
]