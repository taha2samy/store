from django.db import models
import uuid
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from category.models import Element,SubElement,Category
import uuid
import random
import time
import random
import time


def gen_uuid():
    return str(uuid.uuid4())



class PhoneNumber(models.Model):
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.number}'



    
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField( blank=True, null=True)
    
    def __str__(self):
        return self.name
    class Meta:
        permissions=[
            ("can_view_supplier_added","Can view supplier what he added"),
            ("can_change_supplier_added","Can change supplier what he added"),
            ("can_delete_supplier_added","Can delete supplier what he added"),
            ("can_view_supplier_all_detail","Can view supplier all detail"),
            ("can_view_supplier_all_detail_add","Can view supplier all detail he add")

        ]

class PurchaseInvoice(models.Model):
    invoice_number = models.CharField(max_length=50,default=gen_uuid, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())

    @total_amount.setter
    def total_amount(self, value):
        pass
    def __str__(self):
        return f'Invoice {self.invoice_number} - {self.supplier}'
    class Meta:
        permissions = [("can_view_purchaseinvoice_added","Can view purchase invoice what he added"),
            ("can_change_purchaseinvoice_added","Can change purchase invoice what he added"),
            ("can_delete_purchaseinvoice_added","Can delete purchase invoice what he added"),
            ("can_view_purchaseinvoice_all_detail","Can view purchase invoice all detail"),
            ("can_view_purchaseinvoice_all_detail_add","Can view purchase invoice all detail he add"),
            ("can_print_purchaseinvoice_print","Can print purchase invoice print"),
            ("can_print_purchaseinvoice_print_add","Can print purchase invoice print he add")

            
            ]


class PurchaseInvoiceItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2,validators=[MinValueValidator(0)])
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField()
    sub_element_quantity = models.PositiveIntegerField( validators=[MinValueValidator(0)],null=True,blank=True)
    
    def get_max_unit_quantity(self):
        return self.category.sub_element_quantity if self.category else 0
    def save(self, *args, **kwargs):
        if (not self.sub_element_quantity or self.sub_element_quantity == 0) and self.category:
            self.sub_element_quantity = self.category.sub_element_quantity
        super().save(*args, **kwargs)
    @property
    def total_price(self):
        if self.quantity is not None and self.purchase_price is not None:
            if self.category and self.category.sub_element_quantity:
                return self.quantity * float(self.purchase_price) * (self.sub_element_quantity / self.category.sub_element_quantity)
            return self.quantity * float(self.purchase_price)
        return 0
    @total_price.setter
    def total_price(self, value):
        pass
    @property
    def category_sub_element_quantity(self):
        if self.category:
            return self.category.sub_element_quantity
        return None
    def __str__(self):
        # Customize this to include the category or other fields you need to show in the form
        return f"{self.category.name if self.category else 'غير محدد'} - عدد {self.category.sub_element if self.category.sub_element else 'فرعي' } {self.category.sub_element_quantity} | سعر بيع الوحدة كاملة {self.purchase_price} "


def uuid_item():
    
    namespace = uuid.NAMESPACE_DNS
    name = "item"
    random_number = random.randint(1000, 9999)
    timestamp = int(time.time())
    

    return uuid.uuid5(namespace, f"{(uuid.uuid4())}+{name}+{random_number}+{timestamp}")

class Store(models.Model):
    invoice_item = models.ForeignKey(PurchaseInvoiceItem,on_delete=models.CASCADE)
    sub_element_quantity = models.PositiveSmallIntegerField()


    
