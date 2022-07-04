from django.urls import path, include

from shop.views import index, product_view, create_product

urlpatterns = [
    path('', index, name="index"),
    path('product/<int:pk>/', product_view, name="view"),
    path('product/create/', create_product, name="create")
]
