from django.db import models
from model_utils.choices import Choices
# Create your models here.


class Product (models.Model):
    def __str__(self):
        return self.identifier+"-"+self.name

    name = models.CharField("Nome", max_length=120)
    description = models.CharField("Descrição",blank=True, max_length=120)
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


class Client(models.Model):
    def __str__(self):
        return self.name

    origin_choices = [
        ('fb', "Facebook"),
        ('ig', "Instagram"),
        ('p', "Pessoal")
    ]
    name = models.CharField("Nome", max_length=120)
    origin = models.CharField("Origem", max_length=2,
                              default='p', choices=origin_choices)


class ProductSize(models.Model):
    def __str__(self):
        return self.product.name + ":" + self.size.desc + ":" + self.lot.name

    size = models.ForeignKey("Size", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
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
        unique_together = ('size', 'product', 'lot')


class Lot(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField("Nome", max_length=120)


class Size(models.Model):
    def __str__(self):
        return self.desc

    desc = models.CharField("Descrição", max_length=120,
                            help_text="Algo que identifique o tamanho, 'P', 'M', etc...")


class Sale(models.Model):
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    def __str__(self):
        return self.client.name

    @property
    def products(self):
        return ProductSale.objects.filter(sale=self)


class ProductSale(models.Model):
    product = models.ForeignKey("ProductSize", on_delete=models.CASCADE)
    price = models.DecimalField("Preço de venda",max_digits=6, decimal_places=2)
    sale = models.ForeignKey("Sale", on_delete=models.CASCADE)
    quantity = models.IntegerField("Quantidade")
    date = models.DateField("Data da compra")
