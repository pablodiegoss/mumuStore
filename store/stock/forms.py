from django.forms import ModelForm, CharField, IntegerField, Form, ValidationError
from .models import Sale, Lot, ProductSize, Size
from django.contrib import admin
from django.forms import TextInput


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = "__all__"


class ProductSaleForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        stock_left = cleaned_data.get('product').stock_left
        if cleaned_data.get('quantity') > stock_left:
            raise ValidationError(
                "Só temos: " + str(stock_left) + " disponíveis."
            )


class ProductSizeForm(ModelForm):
    stock_left = CharField(max_length=120)
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
