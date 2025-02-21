from django_filters.views import FilterView
from purchases.models import Supplier
from purchases.filters.supplier import SupplierFilter
from django.urls import reverse_lazy
from extra_views import CreateWithInlinesView,UpdateWithInlinesView
from extra_views.generic import GenericInlineFormSetFactory
from purchases.forms.supplier import PhoneNumberForm,SupplierForm
from purchases.models import PhoneNumber,Supplier
from django.forms import modelformset_factory
from django.shortcuts import redirect
from purchases.models import Supplier, PhoneNumber
from django.views.generic import DeleteView,DetailView

from django.contrib.contenttypes.models import ContentType


class SupplierListView(FilterView):
    model = Supplier
    form_class=SupplierForm
    template_name = 'html/supplier/list.html'
    context_object_name = 'suppliers'
    paginate_by = 10
    filterset_class = SupplierFilter  # استخدام الفلتر

    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort',None)
        if sort:
           queryset= queryset.order_by(sort)
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

class SupplierCreateView(CreateWithInlinesView):
    model = Supplier
    form_class=SupplierForm
    inlines = [PhoneNumberInline]
    template_name = 'html/supplier/form.html'
    success_url = reverse_lazy('supplier_list')
    def get_queryset(self):
        return super().get_queryset().order_by("name")

class SupplierUpdateView(UpdateWithInlinesView):
    model = Supplier
    form_class=SupplierForm
    inlines = [PhoneNumberInline]
    template_name = 'html/supplier/form.html'
    success_url = reverse_lazy('supplier_list')

class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'html/supplier/delete.html'
    success_url = reverse_lazy('supplier_list')


class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'html/supplier/detail.html'
    context_object_name = 'supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phone_numbers'] = PhoneNumber.objects.filter(
            content_type=ContentType.objects.get_for_model(Supplier),
            object_id=self.object.id
        )
        return context
