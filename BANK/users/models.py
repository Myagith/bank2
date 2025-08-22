from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CLIENT = 'CLIENT', 'Client'

    role = models.CharField(max_length=16, choices=Role.choices, default=Role.CLIENT)
    can_login = models.BooleanField(
        default=False,
        help_text="Only users created/verified via the app can log into the front-end.",
    )
    email_verified_at = models.DateTimeField(null=True, blank=True)

    # 2FA OTP fields
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_expires_at = models.DateTimeField(null=True, blank=True)

    def mark_email_verified(self):
        self.email_verified_at = timezone.now()
        self.save(update_fields=["email_verified_at"]) 

    @property
    def is_admin(self) -> bool:
        return self.role == self.Role.ADMIN
