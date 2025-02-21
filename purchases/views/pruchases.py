from django_filters.views import FilterView 
from purchases.models import PurchaseInvoice,PurchaseInvoiceItem
from purchases.filters.pruchases import PurchaseInvoiceFilter
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from purchases.models import Supplier
from extra_views import InlineFormSetFactory
from extra_views import CreateWithInlinesView,UpdateWithInlinesView
from django.urls import reverse_lazy
from purchases.forms.purchases import PurchaseInvoiceForm, PurchaseInvoiceItemForm
from django.views.generic import DetailView,DeleteView
from purchases.models import PurchaseInvoice, PurchaseInvoiceItem
from django.db.models import Sum
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


class PurchaseInvoiceDetailView(DetailView):
    model = PurchaseInvoice
    template_name = 'html/purchases/detail.html'  
    context_object_name = 'invoice'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        item = PurchaseInvoiceItem.objects.filter(invoice=self.object)
        context['items'] = item
        context['total_price'] = sum(item.total_price for item in item)

        return context

class PurchaseInvoiceDeleteView(SuccessMessageMixin,DeleteView):
    model = PurchaseInvoice
    template_name = 'html/purchases/delete.html'  
    context_object_name = 'invoice'  
    success_url = reverse_lazy('purchase_list')  



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = PurchaseInvoiceItem.objects.filter(invoice=self.object)
        context['items'] = item
        context['total_price'] = sum(item.total_price for item in item)

        return context
        # First, delete the invoice
    def get_success_message(self,cleaned_data):
        return f"تم حذف الفاتورة بنجاح {self.object.invoice_number}"

class PurchaseInvoiceListView(FilterView):
    model = PurchaseInvoice
    template_name = 'html/purchases/list.html'
    paginate_by = 10
    filterset_class = PurchaseInvoiceFilter
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
        total_amount=Sum(
                ExpressionWrapper(
                    F('items__quantity') *1000* F('items__purchase_price') * (
                        (F('items__sub_element_quantity')/F("items__category__sub_element_quantity"))
                    ),
                    output_field=FloatField()
                )
            )
        )
        queryset=queryset.order_by('purchase_date')
        sort = self.request.GET.get('sort')
        if sort:
             queryset = queryset.order_by(sort)
        for i in queryset:
            print(i.total_amount)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplier_queryset'] = Supplier.objects.all()
        return context
    


class InvoiceItem(InlineFormSetFactory):
    model = PurchaseInvoiceItem
    factory_kwargs = {'extra': 1, 'max_num': 400,
                      'can_order': False, 'can_delete': True}
    form_class = PurchaseInvoiceItemForm


class PurchaseInvoiceUpdateView(SuccessMessageMixin,UpdateWithInlinesView):
    model = PurchaseInvoice
    form_class = PurchaseInvoiceForm
    inlines = [InvoiceItem]
    template_name = 'html/purchases/form.html'
    success_url = reverse_lazy('purchase_list') 
    def get_success_message(self, cleaned_data):
        return f"تم تعديل الفاتور بنجاح رقم {self.object.invoice_number}"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        item =PurchaseInvoiceItem.objects.filter(invoice=self.object)
        context["total_price"]=sum(item.total_price for item in item)
        return context

class PurchaseInvoiceCreateView(SuccessMessageMixin,CreateWithInlinesView):
    model = PurchaseInvoice
    form_class = PurchaseInvoiceForm
    inlines = [InvoiceItem]
    template_name = 'html/purchases/form.html'
    factory_kwargs = {'extra': 1, 'max_num': None,
                      'can_order': False, 'can_delete': False}

    success_url = reverse_lazy('purchase_list')
    def get_success_message(self, cleaned_data):
        return f"تم انشاء الفاتورة  بنجاح رقم {self.object.invoice_number}"
  

    

