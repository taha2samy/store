from django.shortcuts import render
from django_filters.views import FilterView
from sales.models import SellsInvoice
from sales.filter.sales import SellsInvoiceFilter
from django.db.models import Sum
from sales.models import Customer,SellsItems
from extra_views import CreateWithInlinesView,UpdateWithInlinesView
from extra_views import InlineFormSetFactory
from sales.forms.sales import SellsItemsForm,SellsInvoiceForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class SellsItemsInline(InlineFormSetFactory):
    model = SellsItems
    form_class = SellsItemsForm
    factory_kwargs = {
        'extra': 1,
        'can_order': False,
        'can_delete': True,
    }


class SellsInvoiceListView(FilterView):
    model = SellsInvoice
    template_name = 'sales/list.html'
    context_object_name = 'invoices'
    paginate_by = 10
    filterset_class = SellsInvoiceFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(total_price=Sum('sellsitems__sell_price'))
        sort = self.request.GET.get('sort',None)
        if sort: 
           queryset = queryset.order_by(sort)
        else:
            queryset = queryset.order_by('-date')

        return queryset  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Create View for SellsInvoice
class SellsInvoiceCreateView(SuccessMessageMixin, CreateWithInlinesView):
    model = SellsInvoice
    inlines = [SellsItemsInline]
    form_class = SellsInvoiceForm
    template_name = 'sales/form.html'
    success_message = "تم إضافة الفاتورة بنجاح"
    success_url = reverse_lazy('invoice_list')

# Update View for SellsInvoice
class SellsInvoiceUpdateView(SuccessMessageMixin, UpdateWithInlinesView):
    model = SellsInvoice
    inlines = [SellsItemsInline]
    form_class = SellsInvoiceForm
    template_name = 'sales/form.html'
    success_message = "تم تعديل الفاتورة بنجاح"
    success_url = reverse_lazy('invoice_list')