from rest_framework import serializers

from shop.models import Product, Order, OrderProduct


class ProductModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id',)


class OrderModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'name', 'user', 'address', 'phone', 'created_at', 'order_products')
