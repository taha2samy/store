import django_filters
from sales.models import SellsInvoice,Customer


class SellsInvoiceFilter(django_filters.FilterSet):
    id=django_filters.NumberFilter(label='معرف')
    date = django_filters.DateFromToRangeFilter(label='التاريخ')
    customer = django_filters.ModelChoiceFilter(field_name='customer', queryset=Customer.objects.all().order_by('name'), label='العميل')
    total_price = django_filters.RangeFilter(label='الإجمالي')
    class Meta:
        model = SellsInvoice
        fields = ["id",'date', 'customer', 'total_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
