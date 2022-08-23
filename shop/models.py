from django.contrib.auth import get_user_model
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
        return reverse('shop:view', kwargs={"pk": self.pk})

    class Meta:
        db_table = "Product"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"





class Order(models.Model):
    name = models.CharField(max_length=50, verbose_name="Имя")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    address = models.CharField(max_length=50, verbose_name="Адрес")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    products = models.ManyToManyField('shop.Product', related_name='orders', verbose_name='Товары',
                                      through='shop.OrderProduct', through_fields=['order', 'product'])
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True, related_name="users",
                              verbose_name="Пользователь")

    def __str__(self):
        return f'{self.name} - {self.phone}'

    class Meta:
        db_table = "Order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderProduct(models.Model):
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE, related_name="order_products",
                                verbose_name="Продукт")
    order = models.ForeignKey("shop.Order", on_delete=models.CASCADE, related_name="order_products",
                              verbose_name="Продукт")
    balance = models.PositiveIntegerField(verbose_name="Количество")


    def __str__(self):
        return f'{self.product.name} - {self.order.name}'

    class Meta:
        db_table = "Order_Product"
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"
