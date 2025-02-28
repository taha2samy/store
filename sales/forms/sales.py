
from sales.models import SellsInvoice,SellsItems
from django import forms
from django.core.exceptions import ValidationError
from sales.models import PurchaseInvoiceItem
from purchases.models import Store
class SellsInvoiceForm(forms.ModelForm):
    class Meta:
        model = SellsInvoice
        fields = ['customer']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control', 'placeholder': 'اختر العميل'}),
        }
        labels = {
            'customer': 'العميل',
        }



class SellsItemsForm(forms.ModelForm):
    category_sub_element_quantity = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={
            'readonly': 'readonly',
            'class': 'form-control',
        })
    )
    category_sell_price = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={
            'readonly': 'readonly',
            'class': 'form-control',
        })
    )

    purchase_invoice_item = forms.ModelChoiceField(
        queryset=PurchaseInvoiceItem.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'اختر عنصر الفاتورة'
        }),
        label="عنصر الفاتورة",
        help_text="اختر العنصر الذي سيتم بيعه من الفاتورة."
    )

    class Meta:
        model = SellsItems
        fields = ['purchase_invoice_item', 'sub_element_quantity', 'sell_price','store_item_n']
        widgets = {
            'sub_element_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الكمية'
            }),
            'store_item_n': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل رقم المنتج المخزني',
                "readonly": "readonly"
            }),
            'sell_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل سعر البيع'
            }),
        }
    def clean(self):
        new_quantity = self.cleaned_data.get('sub_element_quantity')
        store_item_n = self.cleaned_data.get('store_item_n') or self.instance.store_item_n
        try:
            old_quantity = SellsItems.objects.get(id=self.instance.id).sub_element_quantity
        except SellsItems.DoesNotExist:
            old_quantity = 0 
        quantity_difference = old_quantity - new_quantity
        print(quantity_difference)
        if quantity_difference > 0:
            pass
        elif quantity_difference < 0:
            try:
                print(store_item_n)
                store = Store.objects.get(id=store_item_n)
                print(store.sub_element_quantity)
                if store.sub_element_quantity >= abs(quantity_difference):
                    pass
                else:
                    self.add_error("sub_element_quantity","لا توجد كمية كافية في المخزن.")
            except Store.DoesNotExist:
                self.add_error("store_item_n","هذا العنصر غير موجود في المخزن.")
        if new_quantity is None or new_quantity <= 0:
            self.add_error("sub_element_quantity", "الكمية يجب أن تكون أكبر من صفر.")
        return super().clean()
    



    def clean_sell_price(self):
        """
        Ensure the sell_price is greater than zero.
        """
        sell_price = self.cleaned_data.get('sell_price')
        if sell_price is not None and sell_price <= 0:
            raise ValidationError("سعر البيع يجب أن يكون أكبر من صفر.")
        return sell_price
    def clean_store_item_n(self):
        store_item_n = self.cleaned_data.get('store_item_n')
        if store_item_n is None:
            raise ValidationError("يجب تحديد رقم المنتج المخزني.")
        return store_item_n

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = False
            field.help_text = False
        if self.instance and self.instance.purchase_invoice_item:
            category = self.instance.purchase_invoice_item.category
            if category:
                self.fields["category_sub_element_quantity"].initial = category.sub_element_quantity
                self.fields["category_sell_price"].initial = category.sell_price
 
 