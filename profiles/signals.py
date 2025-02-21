from .models import User,Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from purchases.models import PhoneNumber

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(pre_delete, sender=Profile)
def delete_phone_numbers(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(Profile)
    PhoneNumber.objects.filter(content_type=content_type, object_id=instance.id).delete()