from django.urls import path
from .views.category import CategoryCreateView,CategoryListView,CategoryDeleteView,CategoryUpdateView
from .views.supplier import SupplierListView,SupplierCreateView,SupplierUpdateView,SupplierDeleteView,SupplierDetailView
from .views.pruchases import PurchaseInvoiceListView,PurchaseInvoiceCreateView,PurchaseInvoiceUpdateView,PurchaseInvoiceDetailView,PurchaseInvoiceDeleteView
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import random
from purchases.models import Category


def search_results(request):
    query = request.GET
    l = query.get('searchable-input',None)
    data = [i for i in Category.objects.filter(name__icontains=l)]

    
    # تمرير النتائج إلى القالب
    return render(request, 'search.html', {'options': data})

def additional_action(request):
    l= request.GET.get("byid")
    s=Category.objects.get(id=int(l))
    if s is not None:
        return render(request, 'html/purchases/tang.html', {"data": s})

    return HttpResponse('<h1></h1>')

    

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/update/<int:pk>/', SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/delete/<int:pk>/', SupplierDeleteView.as_view(), name='supplier_delete'),
    path('suppliers/detail/<int:pk>/', SupplierDetailView.as_view(), name='supplier_detail'),
    path('purchases/', PurchaseInvoiceListView.as_view(), name='purchase_list'),
    path('purchases/create/', PurchaseInvoiceCreateView.as_view(), name='purchase_create'),
    path('purchases/update/<int:pk>/', PurchaseInvoiceUpdateView.as_view(), name='purchase_update'),
    path('purchases/detail/<int:pk>/', PurchaseInvoiceDetailView.as_view(), name='purchase_detail'),
    path('purchases/delete/<int:pk>/', PurchaseInvoiceDeleteView.as_view(), name='purchase_delete'),

    path('update_button/', search_results, name='search_results'),
    path("sssss/",additional_action,name="additional_action")


    


]