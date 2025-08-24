from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),  # Admin-only via decorator
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('otp/', views.otp_verify, name='otp_verify'),
]