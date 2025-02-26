from django.db.models.signals import pre_save,pre_delete
from django.dispatch import receiver
from .models import SellsItems,Customer
from django.core.exceptions import ObjectDoesNotExist
from purchases.models import Store,PhoneNumber
from django.contrib.contenttypes.models import ContentType


@receiver(pre_delete, sender=Customer)
def delete_phone_numbers(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(Customer)
    PhoneNumber.objects.filter(content_type=content_type, object_id=instance.id).delete()

@receiver(pre_save, sender=SellsItems)
def update_store_item(sender, instance, **kwargs):
    if instance.pk is None:
        try:
            store = Store.objects.get(id=instance.store_item_n)
            if store.sub_element_quantity >= instance.sub_element_quantity:
                store.sub_element_quantity -= instance.sub_element_quantity
                instance.store_item_n = store.pk
                store.save()
            else:
                raise ValueError("لا توجد كمية كافية في المتجر.")
        except ObjectDoesNotExist:
            raise ValueError("هذا العنصر غير موجود في المتجر.")
    else:
        previous_instance = SellsItems.objects.get(id=instance.pk)
        quantity_difference = previous_instance.sub_element_quantity - instance.sub_element_quantity
        
        if quantity_difference > 0:
            store, created = Store.objects.get_or_create(id=instance.store_item_n, defaults= {'sub_element_quantity':0,"invoice_item":instance.purchase_invoice_item})
            store.sub_element_quantity += quantity_difference
            store.id=instance.store_item_n
            store.save()
            
        if quantity_difference < 0:
            quantity_to_deduct = abs(quantity_difference)
            try:
                store = Store.objects.get(id=instance.store_item_n)
                if store.sub_element_quantity >= quantity_to_deduct:
                    store.sub_element_quantity -= quantity_to_deduct
                    store.save()
                else:
                    raise ValueError("لا توجد كمية كافية في المتجر.")
            except Store.DoesNotExist:
                raise ValueError("هذا العنصر غير موجود في المتجر.")@receiver(pre_delete, sender=SellsItems)

@receiver(pre_delete, sender=SellsItems)
def if_delete_store_item(sender, instance, **kwargs):
    store,created = Store.objects.get_or_create(id=instance.store_item_n,defaults= {'sub_element_quantity':0,"invoice_item":instance.purchase_invoice_item})
    store.sub_element_quantity += instance.sub_element_quantity
    if created:
        store.id=instance.store_item_n
    store.save()