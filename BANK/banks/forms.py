from django import forms
from .models import Bank


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ["name", "country", "city", "email", "phone"]

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if Bank.objects.exclude(pk=self.instance.pk).filter(name__iexact=name).exists():
            raise forms.ValidationError("A bank with this name already exists.")
        return name