from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from shop.forms import ProductForm
from shop.models import Product, STATUS_CODE


def index(request):
    product = Product.objects.order_by("category")
    context = {"products": product}
    return render(request, "index.html", context)


def product_view(request, **kwargs):
    pk = kwargs.get("pk")
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_view.html", {'product': product})


def create_product(request):
    if request.method == "GET":
        form = ProductForm()
        return render(request, "create.html", {'category': STATUS_CODE, "form": form})
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
