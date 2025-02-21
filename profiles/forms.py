from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'اسم المستخدم',
        }),
        label='اسم المستخدم',
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'البريد الإلكتروني',
        }),
        label='البريد الإلكتروني',
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'كلمة المرور (اتركه فارغاً إذا لم ترغب في التغيير)',
        }),
        label='كلمة المرور',
    )

    class Meta:
        model = Profile
        fields = ['image', 'name_in_arabic', 'full_name_in_arabic', 'national_id']
        labels = {
            'image': 'الصورة الشخصية',
            'name_in_arabic': 'الاسم باللغة العربية',
            'full_name_in_arabic': 'الاسم الكامل باللغة العربية',
            'national_id': 'الرقم القومي',
        }
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'name_in_arabic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الاسم باللغة العربية',
            }),
            'full_name_in_arabic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الاسم الكامل باللغة العربية',
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل رقم الهوية الوطنية',
            }),
        }

    def __init__(self, *args, **kwargs):
        # Initialize the form and set the initial values for User fields
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        # Override the save method to update related User fields
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile.save()
        return profile
