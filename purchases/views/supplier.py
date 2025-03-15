from django_filters.views import FilterView
from purchases.models import Supplier
from purchases.filters.supplier import SupplierFilter
from django.urls import reverse_lazy
from extra_views import CreateWithInlinesView,UpdateWithInlinesView
from extra_views.generic import GenericInlineFormSetFactory
from purchases.forms.supplier import PhoneNumberForm,SupplierForm
from purchases.models import PhoneNumber,Supplier
from purchases.models import Supplier, PhoneNumber
from django.views.generic import DeleteView,DetailView
from django.contrib.contenttypes.models import ContentType
from guardian.mixins import PermissionListMixin,PermissionRequiredMixin,LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from guardian.shortcuts import assign_perm



class SupplierListView(PermissionListMixin,LoginRequiredMixin,FilterView):
    model = Supplier
    form_class=SupplierForm
    template_name = 'html/supplier/list.html'
    context_object_name = 'suppliers'
    paginate_by = 10
    filterset_class = SupplierFilter
    permission_required="purchases.view_supplier"  
    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort',None)
        if sort and queryset.exists():
           queryset= queryset.order_by(sort)
        elif queryset.exists():
            queryset= queryset.order_by("name")
            
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort = self.request.GET.get('sort')
        return context
    

class PhoneNumberInline(GenericInlineFormSetFactory):
    model = PhoneNumber
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    factory_kwargs = {'extra': 1, 'max_num': 20,
                      'can_order': True, 'can_delete': True}

    form_class = PhoneNumberForm

class SupplierCreateView(PermissionRequiredMixin,SuccessMessageMixin,LoginRequiredMixin,CreateWithInlinesView):
    model = Supplier
    form_class=SupplierForm
    inlines = [PhoneNumberInline]
    template_name = 'html/supplier/form.html'
    success_url = reverse_lazy('supplier_list')
    login_url =reverse_lazy("permission_denied",kwargs={"exception":"غير مصرح لك بانشاء مورد"})
    permission_required="purchases.add_supplier"
    accept_global_perms=True
    success_message = "تم إضافة المورد بنجاح"
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.has_perm('purchases.can_view_supplier_added'):
            assign_perm('purchases.view_supplier', self.request.user, self.object)
        if self.request.user.has_perm('purchases.can_change_supplier_added'):
            assign_perm('purchases.change_supplier', self.request.user, self.object)
        if self.request.user.has_perm('purchases.can_delete_supplier_added'):
            assign_perm('purchases.delete_supplier', self.request.user, self.object)
        if self.request.user.has_perm('purchases.can_view_supplier_all_detail_add'):
            assign_perm('can_view_supplier_all_detail', self.request.user, self.object)
        return response
        
    def get_permission_object(self):
        return None
    def get_queryset(self):
        return super().get_queryset().order_by("name")

class SupplierUpdateView(PermissionRequiredMixin,SuccessMessageMixin,LoginRequiredMixin,UpdateWithInlinesView):
    model = Supplier
    form_class=SupplierForm
    inlines = [PhoneNumberInline]
    template_name = 'html/supplier/form.html'
    success_url = reverse_lazy('supplier_list')
    login_url = reverse_lazy("permission_denied",kwargs={"exception":"غير مصرح له بتعديل على هذا المورد"})
    permission_required="purchases.change_supplier"
    success_message = "تم تعديل المورد بنجاح"
    accept_global_perms=True

class SupplierDeleteView(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    model = Supplier
    template_name = 'html/supplier/delete.html'
    success_url = reverse_lazy('supplier_list')
    accept_global_perms=True
    login_url=reverse_lazy("permission_denied",kwargs={"exception":"غير مصرح له لحذف هذا المورد"})
    permission_required="purchases.delete_supplier"
    
    


class SupplierDetailView(PermissionRequiredMixin,LoginRequiredMixin,DetailView):
    model = Supplier
    template_name = 'html/supplier/detail.html'
    context_object_name = 'supplier'
    permission_required="purchases.can_view_supplier_all_detail"
    login_url=reverse_lazy("permission_denied",kwargs={"exception":"ليس لك اذن بالوصول"})
    accept_global_perms=True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phone_numbers'] = PhoneNumber.objects.filter(
            content_type=ContentType.objects.get_for_model(Supplier),
            object_id=self.object.id)
        return context
