from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from shop.forms import ProductForm
from shop.models import Product, STATUS_CODE


def index(request):
    product = Product.objects.order_by("category")
    context = {"products": product}
    return render(request, "products/index.html", context)


def product_view(request, **kwargs):
    pk = kwargs.get("pk")
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_view.html", {'product': product})


def create_product(request):
    if request.method == "GET":
        form = ProductForm()
        return render(request, "products/create.html", {'category': STATUS_CODE, "form": form})
    else:
        form = ProductForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            category = form.cleaned_data.get("category")
            balance = form.cleaned_data.get("balance")
            price = form.cleaned_data.get("price")
            description = form.cleaned_data.get("description")
            Product.objects.create(name=name, category=category, balance=balance, price=price,
                                   description=description)
            return redirect("index")
        return render("create.html", {"form": form})


def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "GET":
        form = ProductForm(initial={
            "name": product.name,
            "category": product.category,
            "balance": product.balance,
            "description": product.description,
            "price": product.price
        })
        return render(request, "products/update.html", {'form': form, 'category': STATUS_CODE})
    else:
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.cleaned_data.get("name")
            product.category = form.cleaned_data.get("category")
            product.balance = form.cleaned_data.get("balance")
            product.price = form.cleaned_data.get("price")
            product.description = form.cleaned_data.get("description")
            product.save()
            return redirect("view", pk=product.pk)
        return render(request, "products/update.html", {'form': form, 'category': STATUS_CODE})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "GET":
        return render(request, "products/delete.html", {"product": product})
    else:
        product.delete()
        return redirect("index")
