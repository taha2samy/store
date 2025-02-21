import django_filters
from sales.models import Customer

class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='الاسم')
    contact_info = django_filters.CharFilter(lookup_expr='icontains', label='معلومات الاتصال')

    class Meta:
        model = Customer
        fields = ['name', 'contact_info']