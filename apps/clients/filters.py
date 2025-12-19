import django_filters
from .models import Client


class ClientFilter(django_filters.FilterSet):
    bank_name = django_filters.CharFilter(field_name='bank__name', lookup_expr='icontains')

    class Meta:
        model = Client
        fields = ['bank_name', 'person_type']
