from django.urls import path
from . import views

app_name = 'comptes'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/client/', views.dashboard_client, name='dashboard_client'),
    path('password/change/', views.change_password, name='change_password'),
]