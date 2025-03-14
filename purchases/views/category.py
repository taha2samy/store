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
from guardian.mixins import LoginRequiredMixin,PermissionListMixin,PermissionRequiredMixin
from guardian.shortcuts import assign_perm

class CategoryListView(LoginRequiredMixin, PermissionListMixin, FilterView):
    model = Category
    template_name = 'html/category/list.html'
    context_object_name = 'categories'
    paginate_by = 10
    filterset_class = CategoryFilter  # Use the filter
    permission_required= 'category.view_category'

    def get_queryset(self):
        queryset = super().get_queryset()
        if queryset:
            sort = self.request.GET.get('sort')
            queryset = queryset.annotate(total_items=Sum('purchaseinvoiceitem__quantity'))
            if sort:
                queryset = queryset.order_by(sort)
            else:
                queryset=queryset.order_by('id')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', '') 

        return context
    

class CategoryCreateView(PermissionRequiredMixin,CreateView,SuccessMessageMixin,LoginRequiredMixin):
    model = Category
    form_class = CategoryForm
    template_name = 'html/category/form.html'
    success_url = reverse_lazy('category_list') 
    login_url=reverse_lazy('permission_denied',kwargs={"exception":"ليس لديك صلاحيات لانشاء صنف جديد"})
    permission_required= 'category.add_category'
    accept_global_perms=True
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.has_perm('category.can_view_category_added'):
            assign_perm('category.view_category', self.request.user, self.object)
        if self.request.user.has_perm('category.can_change_category_added'):
            assign_perm('category.change_category', self.request.user, self.object)
        if self.request.user.has_perm('category.can_delete_category_added'):
            assign_perm('category.delete_category', self.request.user, self.object)
        return response
    def get_permission_object(self):
        return None
    def get_success_message (self,cleaned_data):
        return f"تم إضافة الصنف {self.object.name} برقم {self.object.id} وسعره {self.object.sell_price} بنجاح!"

class CategoryUpdateView(PermissionRequiredMixin,LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'html/category/form.html'
    success_url = reverse_lazy('category_list') 
    login_url=reverse_lazy('permission_denied',kwargs={"exception":"ليس لديك صلاحيات كافية لتعديل على هذا العنصر"})
    permission_required="category.change_category"
    def get_success_message (self,cleaned_data):
        return f"تم تعديل الصنف {self.object.name} برقم {self.object.id} وسعره {self.object.sell_price} بنجاح!"

class CategoryDeleteView(SuccessMessageMixin,LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Category
    template_name = 'html/category/delete.html'
    success_url = reverse_lazy('category_list')
    permission_required = "category.delete_category"
    login_url = reverse_lazy('permission_denied', kwargs={'exception': 'ليس لديك صلاحيات لحذف هذا الصنف'})

    def get_success_message (self,cleaned_data):
        return f"تم حذف الصنف {self.object.name} برقم {self.object.id} وسعره {self.object.sell_price} بنجاح!"
