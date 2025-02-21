from django.db.models.signals import pre_save,pre_delete
from django.dispatch import receiver
from .models import SellsItems,Customer,
from django.core.exceptions import ObjectDoesNotExist
from purchases.models import Store,PhoneNumber
from django.contrib.contenttypes.models import ContentType


@receiver(pre_delete, sender=Customer)
def delete_phone_numbers(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(Customer)
    PhoneNumber.objects.filter(content_type=content_type, object_id=instance.id).delete()

@receiver(pre_save, sender=SellsItems)
def update_store_item(sender, instance, **kwargs):
    if instance.pk is None:  # New instance
        if not instance.store_item:
            raise ValueError("You must provide a store_item before saving a new SellsItems instance.")

        if instance.store_item.sub_element_quantity < instance.sub_element_quantity:
            raise ValueError("Not enough quantity in store_item.")
        else:
            instance.store_item.sub_element_quantity -= instance.sub_element_quantity
            if instance.store_item.sub_element_quantity == 0:
                # Instead of deleting the store_item, set its quantity to 0
                instance.store_item.sub_element_quantity = 0
            instance.store_item.save()

    else:  # Updating an existing instance
        try:
            old_instance = SellsItems.objects.get(pk=instance.pk)
        except ObjectDoesNotExist:
            raise ValueError("The original SellsItems instance does not exist.")

        old_quantity = old_instance.sub_element_quantity
        new_quantity = instance.sub_element_quantity

        if instance.store_item:
            if old_quantity > new_quantity:  # Quantity decreased
                instance.store_item.sub_element_quantity += (old_quantity - new_quantity)
                instance.store_item.save()
            elif new_quantity > old_quantity:  # Quantity increased
                difference = new_quantity - old_quantity
                if difference > instance.store_item.sub_element_quantity:
                    raise ValueError("Not enough quantity in store.")
                instance.store_item.sub_element_quantity -= difference
                if instance.store_item.sub_element_quantity == 0:
                    # Set the quantity to 0 instead of deleting
                    instance.store_item.sub_element_quantity = 0
                instance.store_item.save()
        else:
            # Creating a new `store_item` when it doesn't exist
            if old_quantity > new_quantity:  # Remaining quantity is positive
                remaining_quantity = old_quantity - new_quantity
                new_store_item = Store.objects.create(
                    invoice_item=instance.purchase_invoice_item,
                    sub_element_quantity=remaining_quantity
                )
                instance.store_item = new_store_item
                instance.store_item.save()
            else:
                raise ValueError("Not enough quantity in store")
            
@receiver(pre_delete, sender=SellsItems)
def restore_store_item(sender, instance, **kwargs):
    """
    Restore the quantity of the associated store_item when a SellsItems instance is deleted.
    """
    if instance.store_item:
        instance.store_item.sub_element_quantity += instance.sub_element_quantity
        instance.store_item.save()
    else:
        new_store_item = Store.objects.create(invoice_item=instance.purchase_invoice_item, sub_element_quantity=instance.sub_element_quantity)
        new_store_item.save()
    
