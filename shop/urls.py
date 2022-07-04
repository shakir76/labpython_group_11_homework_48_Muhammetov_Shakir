from django.urls import path, include

from shop.views import index, product_view

urlpatterns = [
    path('', index, name="index"),
    path('product/<int:pk>/', product_view, name="view")
]
