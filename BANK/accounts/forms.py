from django import forms
from .models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["customer", "number", "type", "status", "balance"]

    def clean_number(self):
        value = self.cleaned_data["number"].strip()
        if Account.objects.exclude(pk=self.instance.pk).filter(number__iexact=value).exists():
            raise forms.ValidationError("Account number already exists.")
        return value