from django.urls import path

from shop.views.products import DeleteProduct, IndexView, ProductView, CreateProduct, UpdateProduct, ProductAdd

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('product/<int:pk>/', ProductView.as_view(), name="view"),
    path('product/create/', CreateProduct.as_view(), name="create"),
    path('product/update/<int:pk>/', UpdateProduct.as_view(), name="update"),
    path('product/delete/<int:pk>/', DeleteProduct.as_view(), name="delete"),
    path('product/<int:pk>/add/cart', ProductAdd.as_view(), name="add_cart"),
]
