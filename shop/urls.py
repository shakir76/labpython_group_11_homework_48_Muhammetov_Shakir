from django.urls import path

from shop.views.products import DeleteProduct, IndexView, ProductView, CreateProduct, UpdateProduct, ProductAdd, \
    CartView, DeleteCart, OrderCreateView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('product/<int:pk>/', ProductView.as_view(), name="view"),
    path('product/create/', CreateProduct.as_view(), name="create"),
    path('product/update/<int:pk>/', UpdateProduct.as_view(), name="update"),
    path('product/delete/<int:pk>/', DeleteProduct.as_view(), name="delete"),
    path('product/<int:pk>/add/cart', ProductAdd.as_view(), name="add_cart"),
    path('cart/', CartView.as_view(), name="cart"),
    path('cart/delete/<int:pk>/', DeleteCart.as_view(), name="cart_delete"),
    path('order/create/', OrderCreateView.as_view(), name="order_create")

]
