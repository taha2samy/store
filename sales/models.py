from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator

from purchases.models import Store,PurchaseInvoiceItem


class Customer(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField( blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    
class SellsInvoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.sell_price for item in self.sellsitems.all())

    @total_price.setter
    def total_price(self, value):
        pass



class SellsItems(models.Model):
    purchase_invoice_item = models.ForeignKey(PurchaseInvoiceItem, on_delete=models.CASCADE, null=True, blank=True)
    sub_element_quantity = models.PositiveSmallIntegerField()
    sells_invoice = models.ForeignKey(SellsInvoice, on_delete=models.CASCADE, null=True, blank=True,related_name='sellsitems')
    store_item_n=models.PositiveBigIntegerField(null=True,blank=True)
    sell_price = models.DecimalField(null=True,blank=True,max_digits=10, decimal_places=2,validators=[MinValueValidator(0.01)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
  


