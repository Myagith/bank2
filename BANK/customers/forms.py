from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["bank", "name", "email", "client_no", "phone"]

    def clean_client_no(self):
        value = self.cleaned_data["client_no"].strip()
        if Customer.objects.exclude(pk=self.instance.pk).filter(client_no__iexact=value).exists():
            raise forms.ValidationError("Client number already exists.")
        return value