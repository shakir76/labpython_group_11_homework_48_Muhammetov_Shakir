from django import forms
from django.core.exceptions import ValidationError
from shop.models import Product, ProductInCart


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'balance', 'price', 'description', 'category']

    def clean_balance(self):
        balance = self.cleaned_data.get("balance")
        if balance < 0:
            raise ValidationError("Количество не может быть меньше  0")
        return balance

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise ValidationError("Цена не может быть меньше  или равна 0")
        return price


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Найти')


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = ProductInCart
        fields = ['balance']
