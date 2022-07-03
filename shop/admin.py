from django.contrib import admin

# Register your models here.
from shop.models import Product


class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'balance']
    list_display_links = ['name']
    list_filter = ['category', ]
    search_fields = ['name', 'category', ]
    fields = ['name', 'category',  'price', 'balance',  'description', ]


#
admin.site.register(Product, ShopAdmin)
