from django.urls import path
from .views import MyLogoutView,ProfileUpdateView,ProfileDetailView,HomeView,LoginView,LogoutView

urlpatterns = [
    path("logout/",LogoutView.as_view(),name="logout"),
    path("ready_logout",MyLogoutView.as_view(),name="logout_reset"),
    path("myprofile/",ProfileDetailView.as_view(),name="profile_detail"),
    path("myprofile_edit/",ProfileUpdateView.as_view(),name="profile_edit"),
    path("home/",HomeView.as_view(),name="home"),
    path("login/",LoginView.as_view(),name="login"),
]
    


