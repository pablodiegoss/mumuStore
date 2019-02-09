from django.contrib import admin
from .models import *
from .forms import ProductSizeForm, ProductSaleForm

class ProductSizeInline(admin.TabularInline):
    form = ProductSizeForm
    model = ProductSize

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fields=[]

class ProductSaleInline(admin.TabularInline):
    form = ProductSaleForm
    model = ProductSale

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines=[
        ProductSizeInline,
    ]

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    fields = []

@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    fields = []

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    fields = []
    inlines=[
        ProductSaleInline,
    ]