from django.contrib import admin
from django.contrib import admin
from .models import Customer, SellsInvoice, SellsItems


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(SellsInvoice)
class SellsInvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date')
    list_filter = ('date',)
    search_fields = ('customer__name',)
    ordering = ('-date',)

@admin.register(SellsItems)
class SellsItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'sells_invoice', 'purchase_invoice_item', 'sub_element_quantity', 'store_item_n')
    list_filter = ('sells_invoice',)
    search_fields = ('sells_invoice__id', 'store_item_n')
    ordering = ('sells_invoice',)

# Ensure you register all models
# admin.site.register(Customer, CustomerAdmin)
# admin.site.register(SellsInvoice, SellsInvoiceAdmin)
# admin.site.register(SellsItems, SellsItemsAdmin)
