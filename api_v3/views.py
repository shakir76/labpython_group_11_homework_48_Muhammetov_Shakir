from django.shortcuts import render

# Create your views here.
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api_v3.serializers import ProductModelsSerializer, OrderModelsSerializer
from shop.models import Product, Order


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(balance__gt=0)
    serializer_class = ProductModelsSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()


class OrderView(APIView):
    serializer_class = OrderModelsSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            order = get_object_or_404(Order, pk=pk)
            order_data = self.serializer_class(order).data
            return Response(order_data)
        orders = Order.objects.all()
        orders_data = self.serializer_class(orders, many=True).data
        return Response(orders_data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def get_permissions(self):
        if self.request.method == "POST":
            return []
        return super().get_permissions()
