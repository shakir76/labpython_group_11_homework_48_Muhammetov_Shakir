from django.urls import path

from shop.views.products import delete_product, IndexView, ProductView, CreateProduct, UpdateProduct

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('product/<int:pk>/', ProductView.as_view(), name="view"),
    path('product/create/', CreateProduct.as_view(), name="create"),
    path('product/update/<int:pk>/', UpdateProduct.as_view(), name="update"),
    path('product/delete/<int:pk>/', delete_product, name="delete")
]
