import django_filters
from purchases.models import Category 
from django.db.models import Sum
import django_filters
from purchases.models import Category,SubElement,Element

class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='الاسم')
    sell_price = django_filters.RangeFilter()
    total_items = django_filters.RangeFilter()
    element=django_filters.ModelChoiceFilter(field_name="element",queryset=Element.objects.all().order_by('name'))
    sub_element = django_filters.ModelChoiceFilter(field_name="sub_element", queryset=SubElement.objects.all().order_by('name'))
    sub_element_quantity = django_filters.RangeFilter()
    
    class Meta:
        model = Category
        fields = ['name', 'sell_price', 'element',"sub_element", "sub_element_quantity"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

 
