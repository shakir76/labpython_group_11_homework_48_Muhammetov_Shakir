from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

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

    class Meta:
        db_table = "Product"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
