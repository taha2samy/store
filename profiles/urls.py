from django.urls import path
from .views import logut_reset,ProfileUpdateView,ProfileDetailView

urlpatterns = [
    path("logout_reset",logut_reset.as_view(),name="logout_reset"),
    path("myprofile/",ProfileDetailView.as_view(),name="profile_detail"),
    path("myprofile_edit/",ProfileUpdateView.as_view(),name="profile_edit")

]