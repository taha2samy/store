from django_filters.views import FilterView
from sales.models import Customer
from sales.filter.customer import CustomerFilter
from django.urls import reverse_lazy
from extra_views import CreateWithInlinesView,UpdateWithInlinesView
from extra_views.generic import GenericInlineFormSetFactory
from purchases.forms.supplier import PhoneNumberForm
from sales.forms.Customer import CustomerForm
from purchases.models import PhoneNumber,Supplier
from purchases.models import Supplier, PhoneNumber
from django.views.generic import DeleteView,DetailView

from django.contrib.contenttypes.models import ContentType


class SupplierListView(FilterView):
    model = Customer
    form_class=CustomerForm
    template_name = 'customer/list.html'
    context_object_name = 'customers'
    paginate_by = 10
    filterset_class = CustomerFilter

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
                      'can_order': False, 'can_delete': True}

    form_class = PhoneNumberForm

class CustomerCreateView(CreateWithInlinesView):
    model = Customer
    form_class=CustomerForm
    inlines = [PhoneNumberInline]
    template_name = 'customer/form.html'
    success_url = reverse_lazy('customer_list')
    def get_queryset(self):
        return super().get_queryset().order_by("name")

class CustomerUpdateView(UpdateWithInlinesView):
    model = Customer
    form_class=CustomerForm
    inlines = [PhoneNumberInline]
    template_name = 'customer/form.html'
    success_url = reverse_lazy('customer_list')

class SupplierDeleteView(DeleteView):
    model = Customer
    template_name = 'customer/delete.html'
    success_url = reverse_lazy('customer_list')


class SupplierDetailView(DetailView):
    model = Customer
    template_name = 'customer/detail.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phone_numbers'] = PhoneNumber.objects.filter(
            content_type=ContentType.objects.get_for_model(Customer),
            object_id=self.object.id
        )
        return context
