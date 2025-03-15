from django_filters.views import FilterView 
from purchases.models import PurchaseInvoice,PurchaseInvoiceItem
from purchases.filters.pruchases import PurchaseInvoiceFilter
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from purchases.models import Supplier,Store
from extra_views import InlineFormSetFactory
from extra_views import CreateWithInlinesView,UpdateWithInlinesView
from django.urls import reverse_lazy
from purchases.forms.purchases import PurchaseInvoiceForm, PurchaseInvoiceItemForm
from django.views.generic import DetailView,DeleteView
from purchases.models import PurchaseInvoice, PurchaseInvoiceItem
from django.db.models import Sum
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from guardian.mixins import PermissionRequiredMixin,PermissionListMixin,LoginRequiredMixin
from guardian.shortcuts import assign_perm


class PurchaseInvoicePrintingView(PermissionRequiredMixin,LoginRequiredMixin,SuccessMessageMixin,DetailView):
    model = PurchaseInvoice
    template_name = 'html/purchases/printing.html'  
    context_object_name = 'invoice'
    login_url=reverse_lazy("permission_denied",kwargs={"exception":"غير مصرج لك بطباعة الفاتورة "})  
    accept_global_perms=True
    permission_required="purchases.can_print_purchaseinvoice_print"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        items= PurchaseInvoiceItem.objects.filter(invoice=self.object)
        context['items'] = Store.objects.filter(invoice_item__in=items).prefetch_related('invoice_item')

        return context
    
class PurchaseInvoiceDetailView(PermissionRequiredMixin,LoginRequiredMixin,SuccessMessageMixin,DetailView):
    model = PurchaseInvoice
    template_name = 'html/purchases/detail.html'  
    context_object_name = 'invoice'  
    permission_required="purchases.can_view_purchaseinvoice_all_detail"
    accept_global_perms=True
    login_url=reverse_lazy("permission_denied",kwargs={"exception":"غير مصرح لك بالوصول على بيانات الفاتورة"})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        item = PurchaseInvoiceItem.objects.filter(invoice=self.object)
        context['items'] = item
        context['total_price'] = sum(item.total_price for item in item)

        return context

class PurchaseInvoiceDeleteView(PermissionRequiredMixin,LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    model = PurchaseInvoice
    template_name = 'html/purchases/delete.html'  
    context_object_name = 'invoice'  
    success_url = reverse_lazy('purchase_list')  
    permission_required="purchases.delete_purchaseinvoice"
    accept_global_perms=True
    login_url=reverse_lazy("permission_denied",kwargs={"exception":"غير مصرح لك في حذف الفاتورة"})
     


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = PurchaseInvoiceItem.objects.filter(invoice=self.object)
        context['items'] = item
        context['total_price'] = sum(item.total_price for item in item)

        return context
        # First, delete the invoice
    def get_success_message(self,cleaned_data):
        return f"تم حذف الفاتورة بنجاح {self.object.invoice_number}"

class PurchaseInvoiceListView(LoginRequiredMixin, PermissionListMixin, FilterView):
    model = PurchaseInvoice
    template_name = 'html/purchases/list.html'
    paginate_by = 10
    filterset_class = PurchaseInvoiceFilter
    permission_required="purchases.view_purchaseinvoice"
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
        sort = self.request.GET.get('sort')
        if sort:
             queryset = queryset.order_by(sort)
        else:
            queryset = queryset.order_by('-purchase_date')

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


class PurchaseInvoiceUpdateView(PermissionRequiredMixin,LoginRequiredMixin,SuccessMessageMixin,UpdateWithInlinesView):
    model = PurchaseInvoice
    form_class = PurchaseInvoiceForm
    inlines = [InvoiceItem]
    template_name = 'html/purchases/form.html'
    success_url = reverse_lazy('purchase_list') 
    permission_required="purchases.change_purchaseinvoice"
    accept_global_perms=True
    login_url=reverse_lazy('permission_denied',kwargs={"exception":"غير مصرح لك بتعديل على فاتورة الشراء"})
    def get_success_message(self, cleaned_data):
        return f"تم تعديل الفاتور بنجاح رقم {self.object.invoice_number}"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        item =PurchaseInvoiceItem.objects.filter(invoice=self.object)
        context["total_price"]=sum(item.total_price for item in item)
        return context

class PurchaseInvoiceCreateView(PermissionRequiredMixin,LoginRequiredMixin,SuccessMessageMixin,CreateWithInlinesView):
    model = PurchaseInvoice
    form_class = PurchaseInvoiceForm
    inlines = [InvoiceItem]
    template_name = 'html/purchases/form.html'
    factory_kwargs = {'extra': 1, 'max_num': None,
                      'can_order': False, 'can_delete': False}
    permission_required="purchases.add_purchaseinvoice"
    accept_global_perms=True
    login_url=reverse_lazy('permission_denied',kwargs={"exception":"غير مصرح لك في إضافة فاتورة الشراء"})
    success_url = reverse_lazy('purchase_list')
    def get_permission_object(self):
        return None
    def get_success_message(self, cleaned_data):
        return f"تم انشاء الفاتورة  بنجاح رقم {self.object.invoice_number}"
    def form_valid(self, form):
        response =  super().form_valid(form)
        if self.request.user.has_perm('purchases.can_view_purchaseinvoice_added'):
            assign_perm('purchases.view_purchaseinvoice', self.request.user, self.object)
        if self.request.user.has_perm('purchases.can_change_purchaseinvoice_added'):
            assign_perm('purchases.change_purchaseinvoice', self.request.user, self.object)
        if self.request.user.has_perm('category.can_delete_purchaseinvoice_added'):
            assign_perm('purchases.delete_purchaseinvoiceitem', self.request.user, self.object)
        if self.request.user.has_perm('can_print_purchaseinvoice_print_add'):
            assign_perm('can_print_purchaseinvoice_print', self.request.user, self.object)

    
    
        return response

  

    

