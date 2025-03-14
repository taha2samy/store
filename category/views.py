from django.shortcuts import render

from django.views.generic import ListView, UpdateView, DeleteView,CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Element,SubElement
from .forms import ElementForm,SubElementForm
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin, LoginRequiredMixin
from django.shortcuts import redirect
from guardian.shortcuts import assign_perm
from django.contrib.messages.views import SuccessMessageMixin

class ElementListView(PermissionListMixin,LoginRequiredMixin, ListView):
    model = Element
    template_name = 'element_list.html'
    context_object_name = 'elements'
    paginate_by = 10
    permission_required = 'category.view_element'

    def get_queryset(self):
        elements = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            return elements.filter(
                Q(name__icontains=query) | Q(detail__icontains=query)
            ).order_by('id')
        return elements.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = Element._meta.db_table
        return context







class ElementUpdateView(PermissionRequiredMixin,SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Element
    form_class = ElementForm
    template_name = 'element_form.html'
    success_url = reverse_lazy('main_element_list')
    permission_required = 'category.change_element'
    login_url = reverse_lazy('permission_denied', kwargs={"exception": "غير مصرح لك بالتعديل على هذا العنصر"})
    success_message = "تم تعديل العنصر بنجاح "
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = Element._meta.db_table
        return context

def permission_denied(request, exception=None,*args,**kwargs):
    
    return render(request, '403.html', {"exception": exception}, status=200)

class ElementCreateView(PermissionRequiredMixin,SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Element
    form_class = ElementForm
    template_name = 'element_form.html' 
    success_url = reverse_lazy('main_element_list') 
    permission_required = 'category.add_element'
    login_url=reverse_lazy('permission_denied',kwargs={"exception":"غير مصرح ليك بانشاء عنصر جديد"})
    accept_global_perms=True
    success_message = "تم انشاء عنصر بنجاح"
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.has_perm('category.can_view_element_added'):
            assign_perm('category.view_element', self.request.user, self.object)
        if self.request.user.has_perm('category.can_change_element_added'):
            assign_perm('category.change_element', self.request.user, self.object)
        if self.request.user.has_perm('category.can_delete_element_added'):
            assign_perm('category.delete_element', self.request.user, self.object)
        return response
    def get_permission_object(self):
        return None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = Element._meta.db_table
        return context
class ElementDeleteView(PermissionRequiredMixin,SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Element
    template_name = 'element_confirm_delete.html'  
    success_url = reverse_lazy('main_element_list')  
    permission_required = 'category.delete_element'
    login_url=reverse_lazy('permission_denied',kwargs={"exception":"غير مصرح لك بمسح هذا العنصر"})
    success_message="تم حذف العنصر بنجاح"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = Element._meta.db_table
        return context


class SubElementListView(PermissionListMixin,LoginRequiredMixin, ListView):
    model = SubElement
    template_name = 'element_list.html'  
    context_object_name = 'elements'    
    paginate_by = 10
    permission_required="category.view_subelement"  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = SubElement._meta.db_table
        return context
    def get_queryset(self):
        elements = super().get_queryset()
        query = self.request.GET.get('q')
        print(elements)  
        if query:
            return elements.objects.filter(
                Q(name__icontains=query) | Q(detail__icontains=query)
            )
        return elements.order_by('id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = Element._meta.db_table
        return context

class SubElementUpdateView(PermissionRequiredMixin,SuccessMessageMixin,UpdateView,LoginRequiredMixin):
    model = SubElement
    form_class = SubElementForm
    template_name = 'element_form.html' 
    success_url = reverse_lazy('sub_element_list')
    permission_required = 'category.change_subelement'
    login_url=reverse_lazy('permission_denied',kwargs={"exception":"غير مصرح بالتعديل على هذا العنصر"})
    success_message = "تم تعديل العنصر بنجاح "
    
    
    
    
    
class SubElementCreateView(PermissionRequiredMixin, SuccessMessageMixin,CreateView, LoginRequiredMixin):
    model = SubElement
    form_class = SubElementForm
    template_name = 'element_form.html' 
    success_url = reverse_lazy('sub_element_list')
    permission_required = 'category.add_subelement'
    accept_global_perms=True
    login_url=reverse_lazy('permission_denied',kwargs={"exception":"غير مصرح لك بانشاء عنصر جديد "})
    success_message= "تم انشاء العنصر بنجاح "
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.has_perm('category.can_view_element_added'):
            assign_perm('category.view_element', self.request.user, self.object)
        if self.request.user.has_perm('category.can_change_element_added'):
            assign_perm('category.change_element', self.request.user, self.object)
        if self.request.user.has_perm('category.can_delete_element_added'):
            assign_perm('category.delete_element', self.request.user, self.object)
        return response
    def get_permission_object(self):
        return None


    
class SubElementDeleteView(PermissionRequiredMixin, SuccessMessageMixin,DeleteView, LoginRequiredMixin):
    model = SubElement
    template_name = 'element_confirm_delete.html'  
    success_url = reverse_lazy('sub_element_list') 
    permission_required = 'category.delete_subelement'
    login_url=reverse_lazy('permission_denied',kwargs={"exception":"غير مصرح لك بمسح هذا العنصر"})
    success_message="تم حذف العنصر بنجاح"

    
    

