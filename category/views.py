from django.shortcuts import render

from django.views.generic import ListView, UpdateView, DeleteView,CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Element,SubElement
from .forms import ElementForm,SubElementForm

class ElementListView(ListView):
    model = Element
    template_name = 'element_list.html'  
    context_object_name = 'elements'    
    paginate_by = 10                    
    def get_context_data(self, **kwargs):
        context=super().get_context_data( **kwargs)
        context["name"]=Element._meta.db_table
        return context
    def get_queryset(self):
        query = self.request.GET.get('q')  
        if query:
            return Element.objects.filter(
                Q(name__icontains=query) | Q(detail__icontains=query)
            ).order_by('id')
        return Element.objects.all().order_by('id')

class ElementUpdateView(UpdateView):
    model = Element
    form_class = ElementForm
    template_name = 'element_form.html' 
    success_url = reverse_lazy('main_element_list') 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = Element._meta.db_table
        return context  
class ElementCreateView(CreateView):
    model = Element
    form_class = ElementForm
    template_name = 'element_form.html' 
    success_url = reverse_lazy('main_element_list')  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = Element._meta.db_table
        return context
class ElementDeleteView(DeleteView):
    model = Element
    template_name = 'element_confirm_delete.html'  
    success_url = reverse_lazy('main_element_list')  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = Element._meta.db_table
        return context

### ----------------------- 
### ----------------------- 

class SubElementListView(ListView):
    model = SubElement
    template_name = 'element_list.html'  
    context_object_name = 'elements'    
    paginate_by = 10                    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = SubElement._meta.db_table
        return context
    def get_queryset(self):
        query = self.request.GET.get('q')  
        if query:
            return SubElement.objects.filter(
                Q(name__icontains=query) | Q(detail__icontains=query)
            )
        return SubElement.objects.all()

class SubElementUpdateView(UpdateView):
    model = SubElement
    form_class = SubElementForm
    template_name = 'element_form.html' 
    success_url = reverse_lazy('sub_element_list')  
class SubElementCreateView(CreateView):
    model = SubElement
    form_class = SubElementForm
    template_name = 'element_form.html' 
    success_url = reverse_lazy('sub_element_list')  
class SubElementDeleteView(DeleteView):
    model = SubElement
    template_name = 'element_confirm_delete.html'  
    success_url = reverse_lazy('sub_element_list')  
   