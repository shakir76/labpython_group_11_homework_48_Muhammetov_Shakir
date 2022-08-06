from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from django.urls import reverse

STATUS_CODE = [('other', 'Разное'), ('keyboard', 'Клавиатура'), ('block', 'Блок питания'),
               ('matrix', 'Матрица'), ('battery', 'Батарейка'), ]


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Наименование")
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Описание")
    category = models.CharField(max_length=50, choices=STATUS_CODE, verbose_name="Категория", default=STATUS_CODE[0][0])
    balance = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Остаток", default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f"{self.id}. {self.name}: {self.category}"

    def get_absolute_url(self):
        return reverse('view', kwargs={"pk": self.pk})

    class Meta:
        db_table = "Product"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class ProductInCart(models.Model):
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE, related_name="product",
                                verbose_name="Продукт")
    balance = models.IntegerField(validators=[MinValueValidator(0)], default=1, verbose_name="Количество", )

    def __str__(self):
        return f"{self.id}. {self.product}: {self.balance}"

    class Meta:
        db_table = "ProductInCart"
        verbose_name = "Продукт в Корзине"
        verbose_name_plural = "Продукты в Корзине"

    def total_product(self):
        return self.balance * self.product.price
