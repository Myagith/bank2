import os
import random
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import User


def generate_otp() -> str:
    return f"{random.randint(0, 999999):06d}"


def send_otp_email(user: User) -> None:
    default_code = os.getenv('DEFAULT_OTP_CODE')
    user.otp_code = default_code if default_code and len(default_code) == 6 else generate_otp()
    user.otp_expires_at = timezone.now() + timedelta(minutes=10)
    user.save(update_fields=["otp_code", "otp_expires_at"])
    app_name = os.getenv('BANK_NAME', 'BANK')
    subject = os.getenv('OTP_EMAIL_SUBJECT', f"{app_name} - Code de connexion")
    template = os.getenv(
        'OTP_EMAIL_BODY',
        "Bonjour {username},\n\nVotre code de connexion est: {code}.\nIl expire dans {expires_minutes} minutes.\n\n{app_name}")
    message = template.format(
        username=user.username,
        code=user.otp_code,
        expires_minutes=10,
        app_name=app_name,
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)


def send_welcome_email(user: User, raw_password: str) -> None:
    app_name = os.getenv('BANK_NAME', 'BANK')
    subject = os.getenv('WELCOME_EMAIL_SUBJECT', f"Bienvenue sur {app_name}")
    template = os.getenv(
        'WELCOME_EMAIL_BODY',
        "Bonjour {username},\n\nVotre compte a été créé.\nIdentifiant: {username}\nMot de passe initial: {password}\n\nMerci d'utiliser {app_name}.")
    message = template.format(username=user.username, password=raw_password, app_name=app_name)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)