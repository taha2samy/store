import django_filters
from purchases.models import Supplier

class SupplierFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='الاسم')
    contact_info = django_filters.CharFilter(lookup_expr='icontains', label='معلومات الاتصال')

    class Meta:
        model = Supplier
        fields = ['name', 'contact_info']