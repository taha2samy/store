from django.shortcuts import render
from purchases.views.supplier import PhoneNumberInline
from extra_views import CreateWithInlinesView,UpdateWithInlinesView
from extra_views.generic import GenericInlineFormSetFactory
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import Profile
from .forms import ProfileForm
from django.views.generic.detail import DetailView
from purchases.models import PhoneNumber
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.shortcuts import redirect


class HomeView(TemplateView):
    template_name="home.html"
    
class LogoutView(LogoutView):
    next_page = reverse_lazy('login')


class MyLogoutView(LoginRequiredMixin, TemplateView):
    template_name = "registration/logout_reset.html"


class ProfileDetailView(LoginRequiredMixin,TemplateView):
    model = Profile
    form_class=ProfileForm
    template_name = 'registration/detail.html'
    def get_context_data(self, **kwargs):
        self.object = self.request.user
        context = super().get_context_data(**kwargs)
        context["profile"]=Profile.objects.get(user=self.object)
        context["phone_numbers"]= PhoneNumber.objects.filter(content_type=ContentType.objects.get_for_model(Profile),
        object_id=self.object.id)
        return context
    
class ProfileUpdateView(LoginRequiredMixin, UpdateWithInlinesView):
    model = Profile
    form_class = ProfileForm
    inlines = [PhoneNumberInline]
    template_name = 'registration/profile_update.html'
    success_url = reverse_lazy('profile_detail')

    def get_object(self, queryset=None):
        # Fetch the profile using the primary key of the logged-in user
        return self.model.objects.get(user_id=self.request.user.id)


class LoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


    