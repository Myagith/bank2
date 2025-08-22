import django_filters
from .models import Bank


class BankFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(lookup_expr='icontains')
    city = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Bank
        fields = ["country", "city"]