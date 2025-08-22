import django_filters
from .models import Customer


class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    client_no = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = ["bank", "name", "email", "client_no"]