from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView

from shop.forms import ProductForm, SearchForm
from shop.models import Product, STATUS_CODE


class IndexView(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"
    ordering = ("category", 'name')
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Product.objects.filter(
                Q(name__icontains=self.search_value) | Q(category__icontains=self.search_value))
        return Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context["query"] = query
            context["search"] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class ProductView(DetailView):
    template_name = "products/product_view.html"
    model = Product


class CreateProduct(CreateView):
    form_class = ProductForm
    template_name = "products/create.html"



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
