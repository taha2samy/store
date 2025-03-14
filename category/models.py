from django.db import models

# Create your models here.
from django.core.validators import MinValueValidator,MaxValueValidator

class SubElement(models.Model):
    name = models.CharField(max_length=100)
    detail = models.TextField(null=True,blank=True)
    def __str__(self):
        return str(self.name)
    class Meta:
        permissions = [
            ("can_view_element_added", "Can view element what he added"),
            ("can_change_element_added", "Can change element what he added"),
            ("can_delete_element_added", "Can delete element what he added"),
        ]

class Element(models.Model):
    name = models.CharField(max_length=100)
    detail = models.TextField(null=True,blank=True)
    def __str__(self):
        return str(self.name)
    class Meta:
        permissions = [
            ("can_view_element_added", "Can view element what he added"),
            ("can_change_element_added", "Can change element what he added"),
            ("can_delete_element_added", "Can delete element what he added"),
        ]

  
class Category(models.Model):
    name = models.CharField(max_length=100)
    element=models.ForeignKey(Element,on_delete=models.SET_NULL,null=True,blank=True)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sub_element = models.ForeignKey(SubElement,on_delete=models.SET_NULL,null=True,blank=True)
    sub_element_quantity = models.PositiveSmallIntegerField()
    @property
    def total_items(self):
        return self.purchaseinvoiceitem_set.aggregate(total=models.Sum('quantity'))['total'] or 0
    @total_items.setter
    def total_items(self, value):
        pass
    def __str__(self):
        return self.name
    class Meta:
        permissions = [
            ("can_view_category_added", "Can view category what he added"),
            ("can_change_category_added", "Can change category what he added"),
            ("can_delete_category_added", "Can delete category what he added"),
        ]