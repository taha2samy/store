from django import template
from profiles.models import Profile
from django.contrib.auth.models import User

register = template.Library()
@register.filter(name="get_profile")
def get_profile(user):
    """Returns the related Profile for a given User or a specific attribute."""
    if isinstance(user, User):
        return Profile.objects.get(user=user)

    return None
@register.filter(name="get_field")
def get_profile_field(profile, field_name):
    """
    get feild
    """
    attr = str(field_name).split(".")
    if profile:
        if len(attr) > 1 :
            output = getattr(profile, attr[0])
            return getattr(output, attr[1], None)            
        
        else:
            return getattr(profile, field_name, None)
    return None
