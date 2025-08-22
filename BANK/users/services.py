import random
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import User


def generate_otp() -> str:
    return f"{random.randint(0, 999999):06d}"


def send_otp_email(user: User) -> None:
    user.otp_code = generate_otp()
    user.otp_expires_at = timezone.now() + timedelta(minutes=10)
    user.save(update_fields=["otp_code", "otp_expires_at"])
    subject = "Your BANK login code"
    message = f"Use this code to complete your login: {user.otp_code}. It expires in 10 minutes."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)