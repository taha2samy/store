from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from .models import PurchaseInvoice, PurchaseInvoiceItem, Store, PhoneNumber, Supplier
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType

@receiver(pre_delete, sender=Supplier)
def delete_phone_numbers(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(Supplier)
    PhoneNumber.objects.filter(content_type=content_type, object_id=instance.id).delete()

@receiver(post_save, sender=PurchaseInvoiceItem)
def post_save_purchase_invoice_item(sender, instance, created, **kwargs):
    if created:
        stores = [
            Store(invoice_item=instance, sub_element_quantity=instance.sub_element_quantity)
            for _ in range(int(instance.quantity))
        ]
        Store.objects.bulk_create(stores)

@receiver(pre_save, sender=PurchaseInvoiceItem)
def pre_save_purchase_invoice_item(sender, instance, **kwargs):
    if instance.pk:
        previous_instance = PurchaseInvoiceItem.objects.get(pk=instance.pk)
        if instance.quantity == previous_instance.quantity:
            pass
        elif instance.quantity > previous_instance.quantity:
            new = instance.quantity - previous_instance.quantity
            stores = [
                Store(invoice_item=instance, sub_element_quantity=instance.sub_element_quantity)
                for _ in range(int(new))
            ]
            Store.objects.bulk_create(stores)
        elif instance.quantity < previous_instance.quantity:
            remove_count = previous_instance.quantity - instance.quantity
            stores_to_remove = Store.objects.filter(invoice_item=instance)[:remove_count]
            if stores_to_remove.count() < remove_count:
                raise ValidationError("Cannot remove more elements than exist.")
            # Convert the queryset to a list and delete each item individually
            stores_to_remove_list = list(stores_to_remove)
            for store in stores_to_remove_list:
                store.delete()

@receiver(pre_delete, sender=PurchaseInvoiceItem)
def pre_delete_purchase_invoice_item(sender, instance, **kwargs):
    stores_to_remove = Store.objects.filter(invoice_item=instance)
    if stores_to_remove.count() < instance.quantity:
        raise ValidationError("Cannot delete PurchaseInvoiceItem because there are not enough related Store elements.")
    # Convert the queryset to a list and delete each item individually
    stores_to_remove_list = list(stores_to_remove)
    for store in stores_to_remove_list:
        store.delete()