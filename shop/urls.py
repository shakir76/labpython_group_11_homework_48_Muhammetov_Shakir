
from django.urls import path, include

from shop.views import index

urlpatterns = [
    path('', index, name="index")
]