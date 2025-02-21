from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from purchases.models import Store,PurchaseInvoiceItem


class Customer(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField( blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    
class SellsInvoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date =models.DateTimeField(auto_now_add=True)

class SellsItems(models.Model):
    
    purchase_invoice_item = models.ForeignKey(PurchaseInvoiceItem, on_delete=models.CASCADE, null=True, blank=True)
    sub_element_quantity = models.PositiveSmallIntegerField()
    sells_invoice = models.ForeignKey(SellsInvoice, on_delete=models.CASCADE, null=True, blank=True)
    store_item=models.OneToOneField(Store, on_delete=models.SET_NULL, blank=True,null=True,related_name="store")

