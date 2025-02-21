from django import forms
from .models import Element, SubElement

class ElementForm(forms.ModelForm):
    class Meta:
        model = Element
        fields = ['name', 'detail']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسم العنصر',
                'maxlength': 100,
            }),
            'detail': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل تفاصيل العنصر',
                'rows': 5,
            }),
        }
        labels = {
            'name': 'اسم العنصر',
            'detail': 'تفاصيل العنصر',
        }
        help_texts = {
            'name': 'العنصر الرئيسي يُقصد به الكيان الأكبر الذي يحتوي على عدة عناصر فرعية، مثل كرتونة البيض التي تحتوي على عدة بيضات.',
            'detail': 'يمكنك إضافة أي تفاصيل إضافية حول العنصر هنا.'
        }


class SubElementForm(forms.ModelForm):
    class Meta:
        model = SubElement
        fields = ['name', 'detail']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسم العنصر الفرعي',
                'maxlength': 100,
            }),
            'detail': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل تفاصيل العنصر الفرعي',
                'rows': 5,
            }),
        }
        labels = {
            'name': 'اسم العنصر الفرعي',
            'detail': 'تفاصيل العنصر الفرعي',
        }
        help_texts = {
            'name': 'العنصر الفرعي يُقصد به الكيان الأصغر الذي يكون جزءًا من العنصر، مثل البيض الذي يوجد في كرتونة البيض.',
            'detail': 'يمكنك إضافة أي تفاصيل إضافية حول العنصر الفرعي هنا.'
        }
