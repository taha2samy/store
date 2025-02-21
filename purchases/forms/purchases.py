from purchases.models import PurchaseInvoice,PurchaseInvoiceItem
from django import forms


from django import forms


class PurchaseInvoiceForm(forms.ModelForm):
    purchase_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'readonly': True,
        }),
        label='تاريخ الشراء',
        required=False,
    )

    class Meta:
        model = PurchaseInvoice
        fields = ['invoice_number', 'supplier']  # لا تضف purchase_date هنا
        labels = {
            'invoice_number': 'رقم الفاتورة',
            'supplier': 'المورد',
        }
        widgets = {
            'supplier': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'اختر المورد',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ضبط القيمة الافتراضية لـ purchase_date
        if self.instance and self.instance.pk:
            self.fields['purchase_date'].initial = self.instance.purchase_date

class PurchaseInvoiceItemForm(forms.ModelForm):


    category_sub_element_quantity = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={
            'readonly': 'readonly',
            'class': 'form-control',
        })
    )


    class Meta:
        model = PurchaseInvoiceItem
        fields = [
            'category', 
            'purchase_price', 
            'quantity', 
            'sub_element_quantity',
        ]
        labels = {
            'category': 'الفئة',
            'purchase_price': 'سعر الشراء',
            'quantity': 'الكمية',
            'sub_element_quantity': 'الكمية الفرعية',
        }
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'اختر الفئة',
            }),
            'purchase_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل سعر الشراء',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الكمية',
            }),
            'sub_element_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الكمية الفرعية',
            }),
        }
        help_texts = {
            'category': 'الصنف',
            'purchase_price': 'سعر الشراء',
            'quantity': 'الكمية',
            'sub_element_quantity': 'الكمية الفرعية',
        }

    def clean_sub_element_quantity(self):
        sub_element_quantity = self.cleaned_data.get('sub_element_quantity')
        category = self.cleaned_data.get('category')  # Access category field from cleaned_data

        if category and sub_element_quantity is not None:
            if category.sub_element_quantity < sub_element_quantity:
                raise forms.ValidationError(
                    f'كده انت بتهزر اساس اعلى حاجة {category.sub_element_quantity}'
                )
            if sub_element_quantity < 0:
                raise forms.ValidationError('الكمية الفرعية يجب أن تكون قيمة موجبة.')
        
        return sub_element_quantity

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity <= 0:
            raise forms.ValidationError('الكمية يجب أن تكون قيمة موجبة أكبر من صفر.')
        return quantity

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = False
            field.help_text = False
        if self.instance and self.instance.category:
            self.fields['category_sub_element_quantity'].initial = self.instance.category_sub_element_quantity

