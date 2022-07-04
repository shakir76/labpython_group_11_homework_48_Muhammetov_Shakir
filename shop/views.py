from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
from shop.models import Product


def index(request):
    product = Product.objects.order_by("category")
    context = {"products": product}
    return render(request, "index.html", context)
