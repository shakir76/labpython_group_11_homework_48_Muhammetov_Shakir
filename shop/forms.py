from django import forms
from django.forms import widgets
from shop.models import STATUS_CODE


class ProductForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, label="Name")
    balance = forms.IntegerField(min_value=0, required=True, label="Balance")
    price = forms.DecimalField(max_digits=7, decimal_places=2, label="Price")
    description = forms.CharField(max_length=2000, required=True, label="Description",
                                  widget=widgets.Textarea(attrs={"cols": 30, "rows": 2}))
    category = forms.ChoiceField(choices=STATUS_CODE, label="Category")

