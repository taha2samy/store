from django.contrib import admin
from django.contrib import admin
from .models import Customer, SellsInvoice, SellsItems


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')
    search_fields = ('name', 'contact_info')
    list_filter = ('name',)


@admin.register(SellsInvoice)
class SellsInvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date')
    search_fields = ('customer__name',)
    list_filter = ('date',)
    date_hierarchy = 'date'


@admin.register(SellsItems)
class SellsItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchase_invoice_item', 'sub_element_quantity', 'sells_invoice', 'store_item')
    search_fields = ('purchase_invoice_item__id', 'sells_invoice__id', 'store_item__id')
    list_filter = ('sells_invoice', 'store_item')
