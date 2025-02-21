from django import forms
from purchases.models import Supplier, PhoneNumber


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_info']
        labels = {
            'name': 'اسم المورد',
            'contact_info': 'معلومات الاتصال',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسم المورد',
            }),
            'contact_info': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل معلومات الاتصال',
                'rows': 3,
            }),
        }
        help_texts = {
            'name': 'أدخل الاسم الكامل للمورد.',
            'contact_info': 'أدخل تفاصيل الاتصال مثل العنوان والبريد الإلكتروني.',
        }


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ['number']
        labels = {
            'number': 'رقم الهاتف',
        }
        help_texts = {
            'number': 'أدخل رقم الهاتف كاملاً بما في ذلك رمز الدولة (مثال: +966123456789)',
        }
        widgets = {
            'number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل رقم الهاتف',
                'min': '0',  # Ensures no negative numbers
            }),
        }

    def clean_number(self):
        number = self.cleaned_data.get('number')
        if not number.isdigit():
            raise forms.ValidationError("يجب أن يحتوي رقم الهاتف على أرقام فقط.")
        return number
