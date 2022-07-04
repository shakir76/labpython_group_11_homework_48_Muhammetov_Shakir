from django.urls import path, include

from shop.views import index, product_view, create_product, update_product, delete_product

urlpatterns = [
    path('', index, name="index"),
    path('product/<int:pk>/', product_view, name="view"),
    path('product/create/', create_product, name="create"),
    path('product/update/<int:pk>/', update_product, name="update"),
    path('product/delete/<int:pk>/', delete_product, name="delete")
]
