from django.forms import ModelForm, CharField, IntegerField, Form
from .models import Sale, Lot, ProductSize, Size
from django.contrib import admin
from django.forms import TextInput


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = "__all__"


class ProductSizeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductSizeForm, self).__init__(*args, **kwargs)
        self.fields['stock_left'] = CharField(
            max_length=120,
            initial=str(self.instance.stock_left),
            widget=TextInput(
                attrs={
                    'readonly': 'readonly'
                }
            )
        )

    class Meta:
        model = ProductSize
        fields = "__all__"
