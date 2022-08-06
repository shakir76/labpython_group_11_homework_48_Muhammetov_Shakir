from django.contrib import admin

# Register your models here.
from shop.models import Product, Order


class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'balance']
    list_display_links = ['name']
    list_filter = ['category', ]
    search_fields = ['name', 'category', ]
    fields = ['name', 'category', 'price', 'balance', 'description', ]


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'address']
    list_display_links = ['name']
    list_filter = ['name', ]
    search_fields = ['name', ]
    fields = ['name', 'phone', 'address', 'created_at',]


#
admin.site.register(Product, ShopAdmin)
admin.site.register(Order, OrderAdmin)
