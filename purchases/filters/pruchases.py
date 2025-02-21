from purchases.models import PurchaseInvoice,Supplier
from django_filters import FilterSet
from django_filters import CharFilter,DateFromToRangeFilter,RangeFilter
class PurchaseInvoiceFilter(FilterSet):
    supplier = CharFilter(field_name='supplier__id', lookup_expr='icontains', label='Supplier Name')
    invoice_number = CharFilter(field_name='invoice_number', lookup_expr='icontains', label='invoice number')
    purchase_date = DateFromToRangeFilter(
        field_name='purchase_date', 
        label='Purchase Date'
    )
    total_amount = RangeFilter(field_name="total_amount", label="Total Price")
    class Meta:
        model = PurchaseInvoice
        fields = ["invoice_number",'supplier', 'purchase_date',"total_amount"]
 
