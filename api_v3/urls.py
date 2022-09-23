from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_v3.views import ProductViewSet, OrderView

app_name = 'api_v3'

router = DefaultRouter()
router.register('product', ProductViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('orders/', OrderView.as_view()),
    path('orders/<int:pk>/', OrderView.as_view())

]
