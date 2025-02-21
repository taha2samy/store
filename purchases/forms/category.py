from django import forms
from purchases.models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', "element", 'sell_price', 'sub_element', 'sub_element_quantity']
        labels = {
            'name': 'اسم الفئة',
            'sell_price': 'سعر البيع',
            "element":"العنصر الرئيسي",
            'sub_element': 'عنصر فرعي',
            'sub_element_quantity': 'الكمية المخصصة للعناصر الفرعية',
        }
        help_texts = {
            'name': 'أدخل اسم الفئة بشكل واضح',
            'sell_price': 'أدخل سعر البيع بالعملة المناسبة (يجب أن يكون رقمًا موجبًا)',
            "element":"  العنصر الرئيسي الخاص بالفئة او الصنف",
            'sub_element': 'اختر العنصر الفرعي المرتبط بالفئة',
            'sub_elment_quantity': 'أدخل الكمية المخصصة للعنصر الفرعي',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسم الفئة'
            }),
            'sell_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل سعر البيع'
            }),
            'sub_element': forms.Select(attrs={
                'class': 'form-control',
            }),
            'sub_element_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الكمية المخصصة للعناصر الفرعية'
            }),
        }
