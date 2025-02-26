from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView
from django.db.models import Sum
from purchases.models import Category,SubElement,Element
from purchases.forms.category import CategoryForm
from purchases.filters.category import CategoryFilter
from django.db.models import Q  # Import Q object for complex lookups
 
class CategoryListView(FilterView):
    model = Category
    template_name = 'html/category/list.html'
    context_object_name = 'categories'
    paginate_by = 10
    filterset_class = CategoryFilter  # استخدام الفلتر

    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort')
        queryset = queryset.annotate(total_items=Sum('purchaseinvoiceitem__quantity') )
        if sort:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', '') 

        return context
    

class CategoryCreateView(SuccessMessageMixin,CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'html/category/form.html'
    success_url = reverse_lazy('category_list')  
    def get_success_message (self,cleaned_data):
        return f"تم إضافة الصنف {self.object.name} برقم {self.object.id} وسعره {self.object.sell_price} بنجاح!"

class CategoryUpdateView(SuccessMessageMixin,UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'html/category/form.html'
    success_url = reverse_lazy('category_list') 
    def get_success_message (self,cleaned_data):
        return f"تم تعديل الصنف {self.object.name} برقم {self.object.id} وسعره {self.object.sell_price} بنجاح!"

class CategoryDeleteView(SuccessMessageMixin,DeleteView):
    model = Category
    template_name = 'html/category/delete.html'
    success_url = reverse_lazy('category_list')
    def get_success_message (self,cleaned_data):
        return f"تم حذف الصنف {self.object.name} برقم {self.object.id} وسعره {self.object.sell_price} بنجاح!"
