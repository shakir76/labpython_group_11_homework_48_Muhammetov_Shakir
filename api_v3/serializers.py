from rest_framework import serializers

from shop.models import Product, Order


class ProductModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id',)


class OrderModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id', "created_at", 'user',)
