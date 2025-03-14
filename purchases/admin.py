from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from .models import (
    Category, 
    Supplier, 
    PurchaseInvoice, 
    PurchaseInvoiceItem, 
    Store, 
    SubElement, 
    PhoneNumber
)

# Customize the PhoneNumber Admin
@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'number')
    search_fields = ('number', 'content_type__model')


@admin.register(SubElement)
class SubElementAdmin(admin.ModelAdmin):
    list_display = ('name',)



# Customize the Category Admin
@admin.register(Category)
class CategoryAdmin(GuardedModelAdmin):
    list_display = ('name', 'sell_price', 'sub_element', 'sub_element_quantity', 'total_items')
    search_fields = ('name', 'sub_element__name')
    list_filter = ('sell_price', 'sub_element')

# Customize the Supplier Admin
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')
    search_fields = ('name', 'contact_info')

# Inline for PurchaseInvoiceItem
class PurchaseInvoiceItemInline(admin.TabularInline):
    model = PurchaseInvoiceItem
    extra = 1
    fields = ('category', 'purchase_price', 'quantity', 'sub_element_quantity', 'display_total_price')
    readonly_fields = ('display_total_price',)

    def display_total_price(self, obj):
        if obj.quantity is not None and obj.purchase_price is not None:
            return f"{obj.total_price:.2f}"
        return "—"
    display_total_price.short_description = 'Total Price'

# Customize the PurchaseInvoice Admin
@admin.register(PurchaseInvoice)
class PurchaseInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'supplier', 'total_amount',"purchase_date")
    search_fields = ('invoice_number', 'supplier__name')
    inlines = [PurchaseInvoiceItemInline]

    def get_readonly_fields(self, request, obj=None):
        # Make total_amount readonly
        return ['total_amount']

# Customize the PurchaseInvoiceItem Admin
@admin.register(PurchaseInvoiceItem)
class PurchaseInvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'purchase_price', 'quantity', 'sub_element_quantity', 'total_price')
    search_fields = ('category__name',)
    readonly_fields = ('total_price',)

# Customize the Store Admin
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id','invoice_item', 'sub_element_quantity')
    search_fields = ('id','invoice_item__category__name',)
    list_filter = ('id','sub_element_quantity',)
