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
    subject = "Your BANK login code"
    message = f"Use this code to complete your login: {user.otp_code}. It expires in 10 minutes."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)


def send_welcome_email(user: User, raw_password: str) -> None:
    subject = "Bienvenue sur la plateforme bancaire"
    message = (
        f"Bonjour {user.username},\n\n"
        f"Votre compte a été créé avec succès.\n"
        f"Identifiant: {user.username}\n"
        f"Mot de passe initial: {raw_password}\n\n"
        f"Veuillez vous connecter et changer votre mot de passe."
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)