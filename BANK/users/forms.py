from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm", "role"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already in use.")
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("password_confirm"):
            self.add_error("password_confirm", "Passwords do not match.")
        return cleaned


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        user = authenticate(username=cleaned.get("username"), password=cleaned.get("password"))
        if not user:
            raise forms.ValidationError("Invalid credentials.")
        if not user.can_login:
            raise forms.ValidationError("Login not allowed for this user.")
        cleaned["user"] = user
        return cleaned


class OTPVerifyForm(forms.Form):
    otp_code = forms.CharField(
        max_length=6,
        validators=[RegexValidator(r"^\d{6}$", "Enter the 6-digit code sent to your email.")],
    )