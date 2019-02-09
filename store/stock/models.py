from django.db import models
from model_utils.choices import Choices
# Create your models here.

class Product (models.Model):
    def __str__(self):
        return self.name
    name = models.CharField("Nome", max_length=120)
    description = models.CharField("Descrição", max_length=120)
    identifier = models.CharField("Código do Produto", max_length=120)
    tag_price = models.FloatField("Preço de Etiqueta")
    bought_price = models.FloatField("Preço de compra")
    gender_choices = [
        ('m', "Masculino"),
        ('f', "Feminino"),
        ('x', "Unisex")
    ]
    gender = models.CharField("Gênero", max_length=1, choices=gender_choices)
    size = models.ManyToManyField("Size", through='ProductSize')
    # category
    # subcategory

class ProductSize(models.Model):
    def __str__(self):
        return self.product.name + ":" + self.size.desc + ":" + self.lot.name

    size = models.ForeignKey("Size", on_delete=models.CASCADE)
    product = models.ForeignKey("Product",on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Quantidade", default=0)
    
    lot = models.ForeignKey('Lot', on_delete=models.CASCADE)
    
    @property
    def stock_left(self):
        sales = ProductSale.objects.filter(product=self)
        sold = 0
        for sale in sales:
            sold += sale.quantity
        return self.quantity - sold

    class Meta:
        unique_together=('size','product','lot')

class Lot(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField("Nome", max_length=120)

class Size(models.Model):
    def __str__(self):
        return self.desc

    desc = models.CharField("Descrição", max_length=120, help_text="Algo que identifique o tamanho, 'P', 'M', etc...")

class Sale(models.Model):
    #name = models.CharField("text", max_length=120, default="")
    @property
    def products(self):
        return ProductSale.objects.filter(sale=self)

class ProductSale(models.Model):
    product = models.ForeignKey("ProductSize", on_delete=models.CASCADE)
    price = models.FloatField("Preço da Venda")
    sale = models.ForeignKey("Sale", on_delete=models.CASCADE)
    quantity = models.IntegerField("Quantidade")
    