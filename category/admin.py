from django.contrib import admin
from .models import Element, SubElement
from guardian.admin import GuardedModelAdmin
@admin.register(Element)
class ElementAdmin(GuardedModelAdmin):
    list_display = ['name', 'detail']
    search_fields = ['name', 'detail']
    list_filter = ['name']
    
# Register your models here.
