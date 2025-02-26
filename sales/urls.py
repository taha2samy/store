from django.urls import path
from .views.customer import SupplierListView,CustomerCreateView,CustomerUpdateView,SupplierDeleteView,SupplierDetailView
from .views.sales import SellsInvoiceListView,SellsInvoiceCreateView,SellsInvoiceUpdateView
urlpatterns = [
    path('customers/', SupplierListView.as_view(), name='customer_list'),
    path('customers/create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/update/<int:pk>/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/delete/<int:pk>/', SupplierDeleteView.as_view(), name='customer_delete'),
    path('customers/detail/<int:pk>/', SupplierDetailView.as_view(), name='customer_detail'),
    path('sales/invoices/', SellsInvoiceListView.as_view(), name='invoice_list'),
    path('sales/invoices/create/', SellsInvoiceCreateView.as_view(), name='invoice_create'),
    path('sales/invoices/update/<int:pk>/', SellsInvoiceUpdateView.as_view(), name='invoice_update'),
]
