from django.db import models
import os
def user_profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.user.username}.{ext}'
    return os.path.join('profile_images', filename)
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    image = models.ImageField(upload_to=user_profile_image_path, null=True, blank=True)
    name_in_arabic = models.CharField(max_length=100, null=True, blank=True)
    full_name_in_arabic = models.CharField(max_length=100, null=True, blank=True)
    national_id = models.CharField(max_length=20, null=True, blank=True)


    def __str__(self):
        return f'{self.user.username} Profile'
    
    